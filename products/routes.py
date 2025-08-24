from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List, Optional
from auth.auth_utils import get_current_user  # dépendance pour l’admin check
from .shemas import ProductModel,ProductCreate,ProductOut,ProductCreate,ProductUpdate


router = APIRouter()



# ==========================
# Dépendance Admin (exemple)
# ==========================
async def admin_required(user=Depends(get_current_user)):
    if not getattr(user, "is_admin", False):
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user

# ==========================
# Routes Produits
# ==========================

# GET /products → lister tous les produits
@router.get("/", response_model=List[ProductOut])
async def list_products():
    products = await ProductModel.find_all().to_list()
    return [
        ProductOut(
            id=str(p.id),
            name=p.name,
            description=p.description,
            price=p.price,
            category=p.category
        ) for p in products
    ]

# GET /products/{product_id} → détail d’un produit
@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: str):
    product = await ProductModel.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductOut(
        id=str(product.id),
        name=product.name,
        description=product.description,
        price=product.price,
        category=product.category
    )

# POST / → crée un produit (admin)

# @router.post("/", response_model=ProductOut)
# async def create_product(
#     product: ProductCreate,
#     user=Depends(admin_required)  # récupère l’utilisateur admin
# ):
#     product_obj = ProductModel(**product.dict())
#     await product_obj.insert()
#     return ProductOut(
#         id=str(product_obj.id),
#         **product.dict()
#     )
@router.post("/", response_model=ProductOut)
async def create_product(product: ProductCreate):
    product_obj = ProductModel(**product.dict())
    await product_obj.insert()
    return ProductOut(
        id=str(product_obj.id),
        **product.dict()
    )


# PUT /products/{product_id} → mettre à jour un produit (admin)
@router.put("/{product_id}", response_model=ProductOut)
async def update_product(product_id: str, product_update: ProductUpdate, user=Depends(admin_required)):
    product = await ProductModel.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    update_data = product_update.dict(exclude_unset=True)
    for k, v in update_data.items():
        setattr(product, k, v)
    await product.save()
    return ProductOut(
        id=str(product.id),
        name=product.name,
        description=product.description,
        price=product.price,
        category=product.category
    )

# DELETE /products/{product_id} → supprimer un produit (admin)
@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: str, user=Depends(admin_required)):
    product = await ProductModel.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await product.delete()
    return

# GET /products/search?q=... → recherche par nom/catégorie
@router.get("/search", response_model=List[ProductOut])
async def search_products(q: str):
    products = await ProductModel.find(
        {"$or": [{"name": {"$regex": q, "$options": "i"}}, {"category": {"$regex": q, "$options": "i"}}]}
    ).to_list()
    return [
        ProductOut(
            id=str(p.id),
            name=p.name,
            description=p.description,
            price=p.price,
            category=p.category
        ) for p in products
    ]
