from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..database import get_db
from datetime import datetime
from sqlalchemy import func, and_

router = APIRouter(prefix="", tags=["products"])

@router.get("/products", response_model=schemas.ProductListResponse)
def read_products(
    search: Optional[str] = Query(None, description="search in title"),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    store_id: Optional[int] = Query(None),
    category: Optional[int] = Query(None),
    status: Optional[bool] = Query(True),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sort_by: Optional[str] = Query(None, description="column name to sort"),
    sort_dir: Optional[str] = Query("desc", description="asc or desc"),
    db: Session = Depends(get_db)
):
    items, total = crud.get_products(db, offset=offset, limit=limit,
                                    search=search, min_price=min_price, max_price=max_price,
                                    store_id=store_id, category=category, status=status,
                                    sort_by=sort_by, sort_dir=sort_dir)
    return {"total": total, "items": items}

@router.get("/products/{product_id}", response_model=schemas.ProductSchema)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.get("/product/{slug}")
def read_product(slug: str, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(
            models.Product.product_slugs == slug
        )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product_array = []
    
    product = product.all()
    p=product[0]

    brand_name = db.get(models.BrandName, p.brand_name).brand_name if p.brand_name else None
    store_name = db.get(models.StoreName, p.store_name).store_name if p.store_name else None
    ID_ = p.id
    image = p.image
    title = p.title
    desc = p.product_description
    spec = p.product_specification
    slugs= p.product_slugs
    product_prices = (
            db.query(
                func.min(models.Product.price).label("min_price"),
                func.max(models.Product.price).label("max_price")
            )
            .filter(models.Product.title.like(f"{title}%"))
            .first()
        )

        

    min_price = product_prices.min_price or 0
    max_price = product_prices.max_price or 0
    store_details_array = []
    store_variant_array = []
    store_list = get_store_list(db)
    for store in store_list:
        store_data = (
            db.query(
                models.Product.store_name,
                models.Product.url,
                func.min(models.Product.price).label("min_price")
            )
            .filter(
                models.Product.title.like(f"{title}%"),
                models.Product.store_name == store["id"]
            )
            .group_by(
                models.Product.store_name,
                models.Product.url
            )
            .first()
        )

        if store_data and store_data.min_price > 0:
            store_details = {
                "site": store["store_name"].capitalize(),
                "logo": store["store_name"].lower(),
                "url": store_data.url,
                "price": store_data.min_price,
            }
            store_details_array.append(store_details)
        

        store_variant = (
            db.query(models.Product)
            .filter(
                models.Product.title.like(f"{title}%"),
                models.Product.store_name == store["id"]
            )
            .all()
        )

        if store_variant:
            store_products_array = [
                {
                    "store": store["store_name"],
                    "logo": store["store_name"].lower(),
                    "url": data.url,
                    "price": data.price,
                    "title": data.title,
                    "img_url": get_image_url(data.image),
                    "description": data.title,
                }
                for data in store_variant
            ]

            store_variant_array.append(store_products_array)  
        
   
    

    # Step 7: Return final JSON response
   # results = {}
    
    record = {
        "id": ID_,
        "image": get_image_url(image),
        "title": title,
        "slugs": slugs,
        "brand": brand_name,
        "store": store_name,
        "description": desc,
        "specifications": spec,
        "minPrice": min_price,
        "maxPrice": max_price,
        "prices": store_details_array,
        "variants": store_variant_array,
        "updated_at": datetime.now(),
    }
        #print("record :", record)
    product_array.append(record)

    #return mobiles
    return {"data": record}
    
    

@router.get("/product-comments/{product_id}")
def comments(product_id: int,db: Session = Depends(get_db)):
    comments = db.query(models.ProductComments).filter(
            models.ProductComments.product_id == product_id
        )
    comments = comments.all()
    comment_records = []
    print("comments :", comments)
    for comment in comments:
        id = comment.id
        name = get_user_name(db, comment.user_id)
        comment_text = comment.comments
        
        comment_record = {
            "id": id,
            "name": name,
            "comment": comment_text,
            "avatar": "user1",
        }
        comment_records.append(comment_record)

    return {"comments": comment_records}

@router.get("/raw-query")
def raw_query(min_price: Optional[float]=Query(None), max_price: Optional[float]=Query(None), db: Session = Depends(get_db)):
    # Example of parameterized raw SQL (safe)
    sql = "SELECT id, title, price FROM product WHERE 1=1"
    params = {}
    if min_price is not None:
        sql += " AND price >= :min_price"
        params['min_price'] = min_price
    if max_price is not None:
        sql += " AND price <= :max_price"
        params['max_price'] = max_price
    result = db.execute(sql, params).mappings().all()
    return {"count": len(result), "rows": [dict(r) for r in result]}


def get_image_url(image_path: str) -> str:
    #base_url = "https://yourcdn.com/images/"
    return f"{image_path}" if image_path else None

# Dummy Store List (replace with actual query or API)
def get_store_list(db: Session):
    stores = db.query(models.StoreName).all()
    return [{"id": s.id, "store_name": s.store_name} for s in stores]

def get_user_name(db: Session, user_id: int):
    user = db.get(models.AuthUser, user_id)
    first_name = user.first_name if user else None
    last_name = user.last_name if user else None
    return f"{first_name} {last_name}".strip() if user else None
