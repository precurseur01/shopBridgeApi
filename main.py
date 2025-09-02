from fastapi import FastAPI
from database import initiate_database
from routers import api_router

app = FastAPI(
    title="ShopBridge API",           # Nom affiché dans Swagger
    description="API pour gérer les utilisateurs, produits et commandes",  
    version="1.0.0",                  # Version de ton API
    contact={
        "name": "Yndris Douanla",
        "url": "https://freedry.dev",
        "email": "contact@freedry.dev",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

@app.on_event("startup")
async def start_db():
    await initiate_database()
    # print("DB init skipped for test")
    

app.include_router(api_router)


@app.get("/ping")
async def ping():
    return {
        "message": "pong",
        "mongo_status": "OK"
    }
