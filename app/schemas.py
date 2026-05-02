from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class StoreSchema(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class ProductSchema(BaseModel):
    id: int
    title: Optional[str]
    url: Optional[str]
    category: Optional[int]
    image: Optional[str]
    price: Optional[float]
    brand_name: Optional[str]
    store_id: Optional[int]
    product_attribute: Optional[str]
    product_description: Optional[str]
    vote_count: Optional[int]
    comment_count: Optional[int]
    created_date: Optional[datetime]
    status: Optional[bool]

    class Config:
        orm_mode = True

class ProductListResponse(BaseModel):
    total: int
    items: List[ProductSchema]
