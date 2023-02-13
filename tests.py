from helpers import *
from datetime import date
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

async def test_date_input(date_testing: list) -> None:
    for i in date_testing:
        try:
            res = isinstance(await get_date_object(i[0]), date)
        except DateFormattingException:
            res = False
        finally:
            print(res == i[1])


async def main():
    await test_date_input(date_testing)



if __name__ == '__main__':
    asyncio.run(main())

#by t.me/yehuda100