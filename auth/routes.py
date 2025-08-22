from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models import UserModel
from auth.schemas import UserCreate, Token, UserOut
from auth.auth_utils import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    # Vérifier si email ou username existe déjà (avec $or en dict)
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
