import helpers as h
import cbs_index as c
from datetime import date
from exceptions import *
import asyncio

date_testing = [
    ("12.02.23", True),
    ("25/8/2021", True),
    ("32/01/22", False),
    ("12.12/23", False),
    ("1.1.22", True),
    ("g2-02-20", False),
    ("12-12-202", False),
    ("12-12-2023h", False),
    ("2020.1.2", False),
    ("12-12-2026", False),
    ("12-12-2002", False),
    ("1-1-19", True)
]

async def test_get_date_object(date_testing: list) -> None:
    for index, item in enumerate(date_testing):
        try:
            res = isinstance(await h.get_date_object(item[0]), date)
        except DateFormattingException:
            res = False
        finally:
            output = "OK!" if res == item[1] else "FAIL"
            print(f"{index + 1}: {output}.")


request_testing = [
    (None, None),
    (9, 2022),
    (12, None),
    (None, 2021),
    (1, 2019)
]

async def test_get_month_index(index_testing: list) -> None:
    for index, item in enumerate(index_testing):
        try:
            res = await c.get_month_index(*item)
        except (JsonParseException, RequestException) as e:
            res = e
        finally:
            print(f"{index + 1}: result -> {res}.")



async def main():
    #await test_get_date_object(date_testing)
    await test_get_month_index(request_testing)



if __name__ == '__main__':
    asyncio.run(main())

#by t.me/yehuda100