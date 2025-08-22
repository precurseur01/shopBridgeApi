# database.py
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models import UserModel
import os

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://yndriswilf:2tFzHhP6f1nPdHEY@cluster0.glnh6jj.mongodb.net/shopbridgedatabase?retryWrites=true&w=majority&appName=Cluster0"
)

async def initiate_database():
    client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=50000)
    try:
        await client.admin.command("ping")
        print("Ping MongoDB réussi !")
    except Exception as e:
        print(f"Erreur ping MongoDB : {e}")
        raise e

    await init_beanie(
        database=client.get_database("shopbridgedatabase"),
        document_models=[UserModel]
    )
