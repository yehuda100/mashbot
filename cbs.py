import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Optional
from exceptions import UnreliableDataException, CBSException


URL = "https://api.cbs.gov.il/index/data/price?id=200010"


async def get_month_interest(month: Optional[datetime] = None) -> dict:
    if month is None:
        month = datetime.today() + relativedelta(months= -1)
    
    payload = {
        "endPeriod": month.strftime("%Y-%m"),
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
    see more-\n {e}.")
        #! this exception does not handled yet !#

    if data["year"] != month.year or data["month"] != month.month:
        raise UnreliableDataException("date {}-{} dos not match to the requested \
    date {}.".format(data["month"], data["year"], month.strftime("%Y-%m")))
        #! this exception does not handled yet !#

    return {"month": datetime(data["year"], data["month"], 1), "percent": percent, "value": value}
