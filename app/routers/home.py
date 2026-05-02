from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..database import get_db
from sqlalchemy import func, and_
from datetime import datetime

router = APIRouter(prefix="", tags=["products"])

# Allow React frontend to connect (important!)


# Utility: Get full image URL
def get_image_url(image_path: str) -> str:
    #base_url = "https://yourcdn.com/images/"
    return f"{image_path}" if image_path else None

# Dummy Store List (replace with actual query or API)
def get_store_list(db: Session):
    stores = db.query(models.StoreName).all()
    return [{"id": s.id, "store_name": s.store_name} for s in stores]




@router.get("/brand-list")
def comments(db: Session = Depends(get_db)):
    brands = db.query(models.BrandName).all()
    return brands

@router.get("/home-mobiles")
def home(db: Session = Depends(get_db)):
#deals_list = product.objects.filter(STATUS=1, CATEGORY=2).select_related('STORE_NAME').order_by('-CREATED_DATE')


    mobiles, total = crud.get_products(db, offset=0, limit=20,
                                    product_attribute='sync_popular', store_name=2, 
                                    category=1, status=True)
    #print(mobiles)
    product_array = []
    deals_list = []  # You can populate this from another source if needed

    # Step 2: Loop over all fetched products
    for mobile in mobiles:
        ID_ = mobile.id
        image = mobile.image
        title = mobile.title
        slugs = mobile.product_slugs
        brand_id = mobile.brand_name
        brand_name = db.get(models.BrandName, brand_id).brand_name if brand_id else None

        
        # Step 3: Calculate min & max price
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
               

        #min_max_price = f"{min_price} - {max_price}"

        # Step 4: Build store list with prices
        store_details_array = []
        store_list = get_store_list(db)

        for store in store_list:
            store_data = (
                db.query(
                    models.Product.store_name,
                    models.Product.url,
                    func.min(models.Product.price).label("min_price")
                )
                .filter(
                    and_(
                        models.Product.title.like(f"{title}%"),
                        models.Product.store_name == store["id"]
                    )
                )
                .group_by(models.Product.store_name, models.Product.url)
                .first()
            )

            if store_data and store_data.min_price > 0:
                store_details = {
                    "site": store["store_name"].capitalize(),
                    "logo": store["store_name"].lower(),
                    "price": store_data.min_price,
                }
                store_details_array.append(store_details)
            
        # Step 5: Count votes & comments
        comments_count = db.query(models.ProductComments).filter(
            models.ProductComments.product_id == ID_
        ).count()

        votes_count = db.query(models.ProductVotes).filter(
            models.ProductVotes.product_id == ID_
        ).count()

        # Step 6: Build product record
        record = {
            "id": ID_,
            "image": get_image_url(image),
            "title": title,
            "slugs": slugs,
            "brand": brand_name,
            "tags": ["all", "popularity"],
            "minPrice": min_price,
            "maxPrice": max_price,
            "prices": store_details_array,
            "comments_count": comments_count,
            "votes_count": votes_count,
            "updated_at": datetime.now(),
        }
        #print("record :", record)
        product_array.append(record)

    # Step 7: Return final JSON response
   # results = {}
    
    #return mobiles
    return {"total": total, "data": product_array, "deals_list": deals_list}



@router.get("/home-deals")
def home(db: Session = Depends(get_db)):
#deals_list = product.objects.filter(STATUS=1, CATEGORY=2).select_related('STORE_NAME').order_by('-CREATED_DATE')


    deals, total = crud.get_products(db, offset=0, limit=10, category=2, status=True)
    #print(mobiles)
    product_array = []
    deals_list = []  # You can populate this from another source if needed

    # Step 2: Loop over all fetched products
    for deal in deals:

        
        ID_ = deal.id
        image = deal.image
        title = deal.title
        slugs = deal.product_slugs
        description = deal.product_description
        store_id = deal.store_name

        #crud.get_store_byId(db, store_id)
        # Step 5: Count votes & comments
        store = db.get(models.StoreName, store_id).store_name
        
        
        # Step 5: Count votes & comments
        comments_count = db.query(models.ProductComments).filter(
            models.ProductComments.product_id == ID_
        ).count()

        votes_count = db.query(models.ProductVotes).filter(
            models.ProductVotes.product_id == ID_
        ).count()

        # Step 6: Build product record
        record = {
            "id": ID_,
            "product": get_image_url(image),
            "name": title,
            "slugs": slugs,
            "description": description,
            "post": "Associated moderator",
            "tag": store,
            "comment": comments_count,
            "likes": votes_count,
            "updated_at": datetime.now(),
        }
        #print("record :", record)
        product_array.append(record)

    # Step 7: Return final JSON response
   # results = {}
    
    #return mobiles
    return {"total": total, "data": product_array}



