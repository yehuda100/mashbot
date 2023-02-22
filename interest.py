from datetime import datetime
from helpers import months_list_from_date
from pytz import timezone
import mongodb as db
import cbs


TZ = timezone("Israel")


async def get_month_percentage(month: datetime) -> float:
    today = datetime.today()
    if datetime.now(TZ) < datetime(today.year, today.month, 15, 18, 30, 0, tzinfo=TZ):
        return 0.0
    if db.does_month_interest_exist(month):
        return await db.get_month_interest(month)["percent"]
    else:
        result = await cbs.get_month_interest(month)
        db.save_month_interest(result)
        return result["percent"]

async def get_interest_from_date(month: datetime) -> float:
    percentage = 0.0
    async for m in months_list_from_date(month):
        percentage += await get_month_percentage(m)
    return percentage


#by t.me/yehuda100