import requests
import mongodb as db
from datetime import date
from datetime import datetime
from pytz import timezone
from typing import Optional
from exceptions import UnreliableDataException, CBSException


URL = "https://api.cbs.gov.il/index/data/price?id=200010"
TZ = timezone("Israel")


async def CBS_get_month_interest(month: Optional[int] = None, year: Optional[int] = None) -> dict:
    if month is None:
        month = date.today().month
    if year is None:
        year = date.today().year
    
    payload = {
        "endPeriod": f"{month}-{year}",
        "last": 1,
        "format": "json",
        "download": False
    }
    try:
        response = requests.get(URL, params=payload)
        json_response = response.json()
    except Exception as e:
        raise CBSException(f"something went wrong with the request, \
        see more- {e}.")
        #! this exception does not handled yet !#

    try:
        data = json_response["month"][0]["date"][0]
        percent, value = data["percent"], data["currBase"]["value"]
    except (KeyError, IndexError) as e:
        raise CBSException(f"coud't parse response to json, \
        see more- {e}.")
        #! this exception does not handled yet !#

    if data["year"] != year or data["month"] != month:
        raise UnreliableDataException("date {}-{} dos not match to the requested \
        date {}-{}.".format(data["month"], data["year"], month, year))

    return {"month": month, "year": year, "percent": percent, "value": value}


def months_list_from_date(month: int, year: int) -> list:
    months_list = []
    for y in range(year, date.today().year + 1):
        if y == date.today().year:
            max_month = date.today().month + 1
        else:
            max_month = 13
        if month > 1 and y == year:
            min_month = month
        else:
            min_month = 1
        for m in range(min_month, max_month):
            months_list.append((m, y))
    return months_list

async def get_month_percentage(month: int, year: int) -> float:
    today = date.today()
    if datetime.now(TZ) < datetime(today.year, today.month, 15, 18, 30, 0, tzinfo=TZ):
        return 0.0
    if db.does_month_interest_exist(month, year):
        return await db.get_month_interest(month, year)
    else:
        try:
            result = await CBS_get_month_interest(month, year)
        except UnreliableDataException:
            return 0.0
        else:
            db.save_month_interest(result)
            return result["percent"]

async def get_interest_from_date(month: int, year: int) -> float:
    percentage = 0.0
    async for m, y in months_list_from_date(month, year):
        percentage += await get_month_percentage(m, y)
    return percentage


#by t.me/yehuda100