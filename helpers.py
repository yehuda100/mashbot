from datetime import datetime
from re import match
from dateutil.relativedelta import relativedelta
from exceptions import DateFormattingException


async def is_date_pattern(str_date: str)-> bool:
    pattern = r"^\d{1,2}[.|\-|/]\d{1,2}[.|\-|/](?:\d{4}|\d{2})$"
    return match(pattern, str_date)

async def date_formatting(str_date: str)-> tuple:
    #split the user input date to datetime args
    splitter = ""
    if match(r"^\d{2}", str_date):
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
    if datetime.today().year < date_args[0] or date_args[0] < 2017:
        raise DateFormattingException(f"year {date_args[0]} out of range.")
    try:
        datetime(*date_args)
    except ValueError as e:
        raise DateFormattingException(f"unable to convert {str_date} to datetime \
        object, exception message - {e}.")
    return date_args

async def get_date_object(str_date: str)-> datetime:
    #get clean and verified date from user input to date object.
    if await is_date_pattern(str_date):
        date_args = await date_formatting(str_date)
        return datetime(*date_args)
    raise DateFormattingException(f"unable to vrified date format in {str_date}.")


def months_list_from_date(month: datetime) -> list:
    months_list = []
    current_month = month
    while month < datetime.today():
        months_list.append(current_month)
        current_month += relativedelta(months=1)
    
    return months_list


#by t.me/yehuda100