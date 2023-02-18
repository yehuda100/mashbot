from datetime import date
import re
from exceptions import DateFormattingException

#?IL = pytz.timezone('Israel') 
# tz needed only in LMS updates.

async def is_date_pattern(str_date: str)-> bool:
    pattern = r"^\d{1,2}[.|\-|/]\d{1,2}[.|\-|/](?:\d{4}|\d{2})$"
    return re.match(pattern, str_date)

async def date_formatting(str_date: str)-> tuple:
    #split the user input date to datetime args
    splitter = ""
    if re.match(r"^\d{2}", str_date):
        splitter = str_date[2]
    else:
        splitter = str_date[1]
    list_date = str_date.split(splitter)
    if not len(list_date) == 3:
        raise DateFormattingException(f"unable to split {str_date} format.")
    if len(list_date[2]) == 2:
        list_date[2] = "20" + list_date[2]
    date_args = tuple(map(int, list_date[::-1]))
    # verify args in range
    if date.today().year < date_args[0] or date_args[0] < 2017:
        raise DateFormattingException(f"year {date_args[0]} out of range.")
    try:
        date(*date_args)
    except ValueError as e:
        raise DateFormattingException(f"unable to convert {str_date} to datetime \
        object, exception message - {e}.")
    return date_args

async def get_date_object(str_date: str)-> date:
    #get clean and verified date from user input to date object.
    if await is_date_pattern(str_date):
        date_args = await date_formatting(str_date)
        return date(*date_args)
    raise DateFormattingException(f"unable to vrified date format in {str_date}.")



#by t.me/yehuda100