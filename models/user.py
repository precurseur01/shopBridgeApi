from beanie import Document
from pydantic import Field, EmailStr
from typing import Optional
from .common import PyObjectId


class UserModel(Document):
    id: Optional[PyObjectId] = Field(alias="_id")
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    hashed_password: str = Field(...)
    is_active: bool = True

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
