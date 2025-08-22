from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Utilisateur à la création (ex: inscription)
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

# Utilisateur en base (sans password en clair)
class UserOut(BaseModel):
    id: Optional[str]
    username: str
    email: EmailStr
    is_active: bool

# Token JWT retourné à la connexion
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Optionnel : données retournées par /me (user connecté)
class UserInDB(UserOut):
    hashed_password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None