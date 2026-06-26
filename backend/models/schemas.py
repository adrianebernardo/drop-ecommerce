from pydantic import BaseModel
from typing import Optional, List

class Product(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    image_url: Optional[str] = None
    image_product: Optional[str] = None
    images: Optional[List[str]] = []
    sizes: Optional[List[str]] = []
    category: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None
    image_product: Optional[str] = None
    images: Optional[List[str]] = None
    sizes: Optional[List[str]] = None
    category: Optional[str] = None