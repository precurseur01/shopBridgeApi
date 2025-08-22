from beanie import Document
from pydantic import Field, EmailStr
from typing import Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class UserModel(Document):  # <-- Hérite de Document ici
    id: Optional[PyObjectId] = Field(alias="_id")
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    hashed_password: str = Field(...)
    is_active: bool = True

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
