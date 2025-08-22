from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models import UserModel
from auth.schemas import UserCreate, Token, UserOut,UserUpdate
from auth.auth_utils import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserOut,summary="Register user")
async def register(user: UserCreate):
    existing_user = await UserModel.find_one({
        "$or": [
            {"email": user.email},
            {"username": user.username}
        ]
    })
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or username already registered")

    user_obj = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    await user_obj.insert()
    return UserOut(
        id=str(user_obj.id),
        username=user_obj.username,
        email=user_obj.email,
        is_active=user_obj.is_active
    )

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UserModel.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# ============================
# GET ALL USERS
# ============================
@router.get("/users", response_model=list[UserOut])
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
@router.put("/users/{user_id}", response_model=UserOut)
async def update_user(user_id: str, user_update: UserUpdate):
    # Chercher l'utilisateur par ID
    user = await UserModel.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Mettre à jour les champs si fournis
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