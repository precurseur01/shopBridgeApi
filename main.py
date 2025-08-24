from fastapi import FastAPI
from database import initiate_database
from auth.routes import router as auth_router
from products.routes import router as products_router
from users.routes import router as users_router

app = FastAPI()

@app.on_event("startup")
async def start_db():
    await initiate_database()
    # print("DB init skipped for test")
    
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(users_router,prefix="/users", tags=["Users"])



@app.get("/ping")
async def ping():
    return {
        "message": "pong",
        "mongo_status": "OK"
    }
