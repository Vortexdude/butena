from motor.motor_asyncio import AsyncIOMotorClient
from app.settings import Config
# client = AsyncIOMotorClient(f"{Config.MONGO_DB_CLIENT}/{Config.DATABASE}")
client = AsyncIOMotorClient("mongodb://127.0.0.1:27017/butena")
beanie_db = client.butena
database = client[Config.MONGO_DATABASE]
collection = database['users']
