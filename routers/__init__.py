from fastapi import APIRouter
from .products import router as products_router
from .users import router as users_router
from .auth import router as auth_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(products_router, prefix="/products", tags=["Products"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
