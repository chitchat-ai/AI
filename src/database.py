from motor.motor_asyncio import AsyncIOMotorClient

from settings import settings


async def get_database():
    client = AsyncIOMotorClient(settings.MONGO_DB_URL)
    return client.mydatabase  # replace `mydatabase` with your database name

