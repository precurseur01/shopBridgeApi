from beanie import Document
from pydantic import Field, EmailStr
from typing import Optional
from .common import PyObjectId


class ProductModel(Document):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None

    class Settings:
        name = "products"  # nom de la collection Mongo