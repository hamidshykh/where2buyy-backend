from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_, desc, asc
from . import models
from typing import List, Tuple, Optional

def get_product(db: Session, product_id: int):
    return db.get(models.Product, product_id)

def get_store_byId(db: Session, store_id: int):
    return db.get(models.StoreName, store_id)
    
def build_products_query(db: Session, search: Optional[str]=None, min_price: Optional[float]=None,
                         max_price: Optional[float]=None, store_id: Optional[int]=None,
                         category: Optional[int]=None, status: Optional[bool]=True,
                         slug: Optional[str]=None, store_name: Optional[int]=True, brand_name: Optional[int]=True,
                         product_attribute: Optional[str]=None, sort_by: Optional[str]=None, sort_dir: Optional[str]="desc"):
    stmt = select(models.Product)

    filters = []
    if search:
        filters.append(models.Product.title.ilike(f"%{search}%"))
    if min_price is not None:
        filters.append(models.Product.price >= min_price)
    if max_price is not None:
        filters.append(models.Product.price <= max_price)
    if slug is not None:
        filters.append(models.Product.slug == slug)    
    if store_name is not None:
        filters.append(models.Product.store_name == store_name)
    if brand_name is not None:
        filters.append(models.Product.brand_name == brand_name)
    if store_id is not None:
        filters.append(models.Product.store_id == store_id)
    if category is not None:
        filters.append(models.Product.category == category)
    if status is not None:
        filters.append(models.Product.status == status)
    if product_attribute is not None:
        filters.append(models.Product.product_attribute == product_attribute)

    if filters:
        stmt = stmt.where(and_(*filters))

    # Sorting
    if sort_by:
        col = getattr(models.Product, sort_by, None)
        if col is not None:
            if sort_dir and sort_dir.lower() == "asc":
                stmt = stmt.order_by(asc(col))
            else:
                stmt = stmt.order_by(desc(col))
    else:
        stmt = stmt.order_by(desc(models.Product.created_date))

    return stmt

def get_products(db: Session, offset: int=0, limit: int=20, **filters) -> Tuple[List[models.Product], int]:
    stmt = build_products_query(db, **filters)
    # count: use a subquery to count results
    total = db.execute(select(func.count()).select_from(stmt.subquery())).scalar_one()
    #items = db.execute(stmt.offset(offset).limit(limit)).scalars().all()
    items = db.execute(stmt.offset(offset)).scalars().all()
    return items, total
