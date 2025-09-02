from fastapi import APIRouter, HTTPException
from models import UserModel
from schemas import UserOut, UserUpdate
from utils.auth_utils import hash_password

router = APIRouter()

# GET ALL USERS (admin uniquement si tu ajoutes une dépendance)
@router.get("/", response_model=list[UserOut], summary="Get all users")
async def get_all_users():
    users = await UserModel.find_all().to_list()
    return [
        UserOut(
            id=str(user.id),
            username=user.username,
            email=user.email,
            is_active=user.is_active
        )
        for user in users
    ]

# UPDATE USER
@router.put("/{user_id}", response_model=UserOut, summary="Update user")
async def update_user(user_id: str, user_update: UserUpdate):
    user = await UserModel.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.username:
        user.username = user_update.username
    if user_update.email:
        user.email = user_update.email
    if user_update.password:
        user.hashed_password = hash_password(user_update.password)
    if user_update.is_active is not None:
        user.is_active = user_update.is_active

    await user.save()
    return UserOut(
        id=str(user.id),
        username=user.username,
        email=user.email,
        is_active=user.is_active
    )

# DELETE USER
@router.delete("/{user_id}", summary="Delete user")
async def delete_user(user_id: str):
    user = await UserModel.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user.delete()
    return {"message": f"User {user_id} deleted successfully"}
