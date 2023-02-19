import helpers as h
import interest as i
from datetime import date
from exceptions import *
import home_owner as ho
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
        res = None
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

async def get_month_CBS_interest(index_testing: list) -> None:
    for index, item in enumerate(index_testing):
        res = None
        try:
            res = await i.CBS_get_month_interest(*item)
        except (CBSException, UnreliableDataException)as e:
            res = e
        finally:
            print(f"{index + 1}: result -> {res}.")

async def home_owner_test():
    home_owner = ho.HomeOwner(1, 'yehuda', date(2023, 1, 10), date(2023, 1, 31), 1625902, 600000)
    print(home_owner.get_next_payment_number(), "\n\n")
    print(home_owner.get_next_payment_amount(3), "\n\n")
    print(home_owner.next_payment(), "\n\n")
    print(home_owner.__dict__)

async def months_list_from_date_test():
    l = [(2, 2023), (1, 2022), (1, 2023), (6, 2022)]
    for d in l:
        print(*d, "->", i.months_list_from_date(*d))

async def main():
    await test_get_date_object(date_testing)
    await get_month_CBS_interest(request_testing)
    await home_owner_test()
    await months_list_from_date_test()



if __name__ == '__main__':
    asyncio.run(main())

#by t.me/yehuda100