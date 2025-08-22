from fastapi import FastAPI
from database import initiate_database
from auth.routes import router as auth_router

app = FastAPI()

@app.on_event("startup")
async def start_db():
    await initiate_database()
    
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API !"}
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/ping")
async def ping():
    return {
        "message": "pong",
        "mongo_status": "OK"
    }
