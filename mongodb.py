from pymongo import DESCENDING
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# Initialize the client instance as a module-level variable
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.MashBot
db.home_owner.createIndex("user_id", unique=True)
db.interest.createIndex("month", unique=True)


async def save_construction_data(data: dict) -> None:
    await db.home_owner.insert_one(data)

async def get_construction_data(user_id: int) -> dict:
    result = await db.home_owner.find_one({"user_id": user_id})
    return result

async def does_construction_data_exist(user_id: int) -> bool:
    result = await db.home_owner.find_one({"user_id": user_id}) is not None
    return result

async def save_month_interest(month: datetime, index: float, percent: float) -> None:
    await db.interest.insert_one({"month": month, "index": index, "percent": percent})

async def get_month_interest(month: datetime) -> dict:
    result = await db.interest.find_one({"month": month})
    return result

async def get_data_from_date(month: datetime) -> dict:
    result = await db.interest.find({"month": {"$gte": month}})

async def does_month_interest_exist(month: datetime) -> bool:
    result = await db.interest.find_one({"month": month}) is not None
    return result

# by t.me/yehuda100