from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models import UserModel,ProductModel
from settings.config import settings

def build_mongo_url() -> str:
    return (
        f"mongodb+srv://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}"
        f"@{settings.MONGO_HOST}/{settings.MONGO_DB}"
        f"?retryWrites=true&w=majority&appName={settings.MONGO_APP_NAME}"
    )

async def initiate_database():
    client = AsyncIOMotorClient(build_mongo_url())

    try:
        await client.admin.command("ping")
        print("✅ Connexion MongoDB réussie !")
    except Exception as e:
        print(f"❌ Erreur de connexion MongoDB : {e}")
        raise e

    await init_beanie(
        database=client.get_database(settings.MONGO_DB),
        document_models=[UserModel, ProductModel]
    )
