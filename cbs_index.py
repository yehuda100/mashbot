import requests
from datetime import date
from typing import Optional
from exceptions import RequestException, JsonParseException, UnreliableResponseException


URL = "https://api.cbs.gov.il/index/data/price?id=200010"


async def get_month_index(month: Optional[int] = None, year: Optional[int] = None) -> dict:
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
        raise RequestException(f"something went wrong with the request, \
        see more- {e}.")

    try:
        data = json_response["month"][0]["date"][0]
        percent, value = data["percent"], data["currBase"]["value"]
    except (KeyError, IndexError) as e:
        raise JsonParseException(f"coud't parse response to json, \
        see more- {e}.")

    if data["year"] != year or data["month"] != month:
        raise UnreliableResponseException("date {}-{} dos not match to the requested \
        date {}-{}.".format(data["month"], data["year"], month, year))

    return {"percent": percent, "value": value}


#? do i want to do request for evry individual paymant ?#
# build function if month interest not exists to get and find it and add to the db

# async def get_interest_from_date(month: int, year: int) -> float:
#     db = db_connection()
#     cursor = db.interest.find({"$and": [{"month": {"$gte": month}}, {"year": {"$gte": year}}]})
#     interest: float = 0.0
#     async for i in cursor:
#         interest += i["precentage"]

#by t.me/yehuda100