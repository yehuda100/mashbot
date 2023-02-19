from motor.motor_asyncio import AsyncIOMotorClient

# Initialize the client instance as a module-level variable
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.MashBot

async def save_home_owner(data: dict) -> None:
    await db.home_owner.insert_one(data)

async def get_home_owner(user_id: int) -> dict:
    result = await db.home_owner.find_one({"user_id": user_id})
    return result

async def does_home_owner_exist(user_id: int) -> bool:
    result = await db.home_owner.find_one({"user_id": user_id}) is not None
    return result

async def save_month_interest(data: dict) -> None:
    await db.interest.insert_one(data)

async def get_month_interest(month: int, year: int) -> dict:
    result = await db.interest.find_one({"month": month, "year": year})
    return result

async def does_month_interest_exist(month: int, year: int) -> bool:
    result = await db.interest.find_one({"month": month, "year": year}) is not None
    return result

# by t.me/yehuda100