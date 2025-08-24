from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models import UserModel
from auth.schemas import UserCreate, Token, UserOut
from auth.auth_utils import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()

# REGISTER
@router.post("/register", response_model=UserOut, summary="Register user")
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

# LOGIN
@router.post("/token", response_model=Token, summary="Login user and get access token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UserModel.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# GET CURRENT USER
@router.get("/me", response_model=UserOut, summary="Get current user profile")
async def get_me(current_user: UserModel = Depends(get_current_user)):
    return UserOut(
        id=str(current_user.id),
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active
    )

@router.post("/password-reset", summary="Request password reset")
async def password_reset(email: str):
    user = await UserModel.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    # Ici tu peux envoyer un mail avec un token (non implémenté)
    return {"message": "Password reset link sent to email (simulation)"}

# ====================================================
# PASSWORD UPDATE
# ====================================================
@router.post("/password-update", summary="Update password (authenticated user)")
async def password_update(new_password: str, current_user: UserModel = Depends(get_current_user)):
    current_user.hashed_password = hash_password(new_password)
    await current_user.save()
    return {"message": "Password updated successfully"}