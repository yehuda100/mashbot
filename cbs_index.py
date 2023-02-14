import json
import requests
from datetime import date
from typing import Optional
from exceptions import *


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
    except Exception as e:
        raise RequestException(f"something went wrong with the request, \
            see more- {e}.")

    try:
        json_response = json.loads(response.text)
        data = json_response["month"][0]["date"][0]
        percent, value = data["percent"], data["currBase"]["value"]
    except (KeyError, IndexError) as e:
        raise JsonParseException(f"coud't parse response to json, \
            see more- {e}.")

    return {"percent": percent, "value": value}


#? do i want to do request for evry individual paymant ?#

#by t.me/yehuda100