import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Optional
from exceptions import UnreliableDataException, CBSException


# Define the API endpoint URL
URL = "https://api.cbs.gov.il/index/data/price?id=200010"

# Define a function to get the interest rate for a given month from the CBS API
#! This function errors are NOT being handel at the moment. !#
async def get_month_interest(month: Optional[datetime] = None) -> dict:
    """
    Get the interest rate for a specific month from the CBS API.

    Args:
        month (datetime, optional): The month to get the interest rate for. If not provided, the interest rate for the previous month will be returned.

    Returns:
        dict: A dictionary containing the month, the interest rate, and the value.
    """
    # If no month is provided, set it to the previous month
    if month is None:
        month = datetime.today() - relativedelta(months= 1)
    # Set the query parameters for the API request
    payload = {
        "endPeriod": month.strftime("%Y-%m"),
        "last": 1,
        "format": "json",
        "download": False
    }

    try:
        # Send a GET request to the API endpoint and parse the JSON response
        response = requests.get(URL, params=payload)
        json_response = response.json()
    except Exception as e:
        # If there is an error with the request, raise a custom CBSException with the error message
        raise CBSException(f"Something went wrong with the request. Error message: {e}.")

    try:
        # Extract the relevant data from the JSON response
        data = json_response["month"][0]["date"][0]
        percent, value = data["percent"], data["currBase"]["value"]
    except (KeyError, IndexError) as e:
        # If there is an error parsing the JSON response, raise a custom CBSException with the error message
        raise CBSException(f"Could not parse response to JSON. Error message: {e}.") 

    # Check if the returned data matches the requested month, raise an exception if not
    if data["year"] != month.year or data["month"] != month.month:
        raise UnreliableDataException(f"Date {data['month']}-{data['year']} does not match the requested date {month.strftime('%Y-%m')}.")
    
    # Return the relevant data in a dictionary
    return {"month": datetime(data["year"], data["month"], 1), "percent": percent, "value": value}


#by t.me/yehuda100