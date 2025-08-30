# store/core/database.py
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "meu_banco"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]