# database.py
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models import UserModel
from products.shemas import ProductModel  # <- ajoute ceci
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")

async def initiate_database():
    client = AsyncIOMotorClient(MONGO_URL)
    try:
        await client.admin.command("ping")
        print("Ping MongoDB réussi !")
    except Exception as e:
        print(f"Erreur ping MongoDB : {e}")
        raise e

    await init_beanie(
        database=client.get_database("shopbridgedatabase"),
        document_models=[UserModel, ProductModel]  # <- ajoute ProductModel ici
    )
