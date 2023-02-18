import motor.motor_asyncio

async def db_connection(): 
    conn_str = f"mongodb://localhost:27017"
    client = motor.motor_asyncio.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=3000)
    # access the DB named MashBot
    db = client.MashBot
    return db

async def save_home_owner(data: dict) -> None:
    db = db_connection()
    db.home_owner.insert_one(**data)

async def get_home_owner(user_id: int) -> dict:
    db = db_connection()
    result = await db.home_owner.find_one({"user_id": user_id})
    return result

async def home_owner_exists(user_id: int) -> bool:
    db = db_connection()
    result = await db.home_owner.find_one({"user_id": user_id}) != None
    return result


async def save_month_interest(**data: dict) -> None:
    db = db_connection()
    db.interest.insert_one(**data)

async def get_month_interest(month: int, year: int) -> dict:
    db = db_connection()
    result = await db.interest.find_one({"month": month, "year": year})
    return result

async def month_interest_exists(month: int, year: int) -> bool:
    db = db_connection()
    result = await db.interest.find_one({"month": month, "year": year}) != None
    return result


# by t.me/yehuda100