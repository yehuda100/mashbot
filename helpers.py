from datetime import datetime
from re import match
from dateutil.relativedelta import relativedelta
from exceptions import DateFormattingException

# Check if the user input date matches a specific format
async def is_date_pattern(str_date: str) -> bool:
    pattern = r"^\d{1,2}[.|\-|/]\d{1,2}[.|\-|/](?:\d{4}|\d{2})$"
    return match(pattern, str_date)

# Format the user input date into a tuple of datetime arguments
async def date_formatting(str_date: str) -> tuple:
    # Split the user input date into its components
    splitter = ""
    if match(r"^\d{2}", str_date):
        splitter = str_date[2]
    else:
        splitter = str_date[1]
    list_date = str_date.split(splitter)
    # Check that the input date is split into three components
    if not len(list_date) == 3:
        raise DateFormattingException(f"unable to split {str_date} format.")
    # If the year is in two-digit format, add "20" to the beginning
    if len(list_date[2]) == 2:
        list_date[2] = "20" + list_date[2]
    # Convert the date components into integers and put them in a tuple
    date_args = tuple(map(int, list_date[::-1]))
    # Check that the year is within a certain range and that the date is valid
    if datetime.today().year < date_args[0] or date_args[0] < 2017:
        raise DateFormattingException(f"year {date_args[0]} out of range.")
    try:
        datetime(*date_args)
    except ValueError as e:
        raise DateFormattingException(f"unable to convert {str_date} to datetime \
        object, exception message - {e}.")
    return date_args

# Convert the user input date into a datetime object
async def get_date_object(str_date: str) -> datetime:
    # Check that the user input date matches the expected format
    if await is_date_pattern(str_date):
        # Format the user input date as a tuple of datetime arguments
        date_args = await date_formatting(str_date)
        # Convert the tuple of datetime arguments into a datetime object
        return datetime(*date_args)
    raise DateFormattingException(f"unable to verify date format in {str_date}.")

# Generate a list of months starting from a given date and ending with the current month
def months_list_from_date(month: datetime) -> list:
    months_list = []
    current_month = month
    # Keep adding months to the list until the current month is the current month of the current year
    while month < datetime.today():
        months_list.append(current_month)
        current_month += relativedelta(months=1)
    return months_list


#by t.me/yehuda100