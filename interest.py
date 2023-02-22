from datetime import datetime
from helpers import months_list_from_date
import mongodb as db
import cbs


async def get_month_percentage(month: datetime) -> float:
    # try to get the month's interest percentage from the database
    result = await db.get_month_interest(month)
    # if not found in the database, get it from CBS API and save to database
    if result is None:
        result = await cbs.get_month_interest(month)
        db.save_month_interest(result)
    # return the month's interest percentage
    return result["percent"]


async def get_interest_from_date(month: datetime) -> float:
    # initialize percentage as 0
    percentage = 0.0
    # loop through all the months from the given month until now
    async for m in months_list_from_date(month):
        # get the interest percentage for the current month
        percentage += await get_month_percentage(m)
    # return the total interest percentage
    return percentage


#by t.me/yehuda100