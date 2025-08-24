from beanie import Document
from pydantic import Field,BaseModel
from typing import Optional,List, Optional

class ProductModel(Document):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None

    class Settings:
        name = "products"  # nom de la collection Mongo

# ==========================
# Schemas
# ==========================
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None

class ProductOut(BaseModel):
    id: str
    name: str
    description: Optional[str]
    price: float
    category: Optional[str]
