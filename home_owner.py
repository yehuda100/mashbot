from math import ceil
from datetime import date
from typing import Optional
from dateutil.relativedelta import relativedelta
import mongodb as db


class HomeOwner():
    """
    class to represent the home owner and
    calculate all the payments and interest attached.
    """
    def __init__(self, user_id: int, name: str, permit_date: date, signing_date: date,\
        price: int, amount_payed: Optional[int]= 0, finish_date: Optional[date]= date(2026, 6, 30),) -> None:

        self.user_id: int = user_id
        self.name: str = name
        self.permit_date: date = permit_date
        self.signing_date: date = signing_date
        self.price: int = price
        self.amount_payed: int = amount_payed
        self.finish_date: date = finish_date


    #! the assumption is the GESHEM payment board!
    @property
    def pay_dates(self) -> dict: 
        return {
            1: self.signing_date + relativedelta(days= +5),
            2: self.signing_date + relativedelta(days= +45),
            3: self.permit_date + relativedelta(months= +6),
            4: self.permit_date + relativedelta(months= +9),
            5: self.permit_date + relativedelta(months= +12),
            6: self.permit_date + relativedelta(months= +15),
            7: self.permit_date + relativedelta(months= +18),
            8: self.permit_date + relativedelta(months= +21),
            9: self.permit_date + relativedelta(months= +24),
            10: self.permit_date + relativedelta(months= +27),
            11: self.permit_date + relativedelta(months= +30),
            12: self.permit_date + relativedelta(months= +33),
            13: self.finish_date
        }

    @property
    def pay_percentage(self) -> dict:
        return {
            1: 0.07,
            2: 0.13,
            3: 0.07,
            4: 0.07,
            5: 0.07,
            6: 0.07,
            7: 0.07,
            8: 0.07,
            9: 0.07,
            10: 0.07,
            11: 0.07,
            12: 0.07,
            13: 0.10,
        }

    @property
    def amount_to_be_payd(self) -> float:
        next_payment = self.get_next_payment_number()
        percentage_to_be_payd = sum(v for k, v in self.pay_percentage.items() if k < next_payment)
        return self.price * percentage_to_be_payd



    def get_next_payment_number(self) -> int:
        for num, day in self.pay_dates.items():
            if date.today() < day:
                return num

    def get_next_payment_amount(self, num: int) -> int:
        if self.amount_payed >= self.amount_to_be_payd:
            return 0
        amount: float = self.price * self.pay_percentage[num]
        if num in (1, 2):
            return ceil(amount)
        interest: float = amount * (1.2 / 100) #! def get_interest needed !#
        return ceil(amount + interest)

    def next_payment(self) -> dict:
        payment_number = self.get_next_payment_number()
        payment_amount = self.get_next_payment_amount(payment_number)
        result = {
            "payment_number": payment_number,
            "payment_amount": payment_amount,
            "payment_date": self.pay_dates[payment_number]
        }
        return result

    async def save(self):
        data = self.__dict__
        db.save_home_owner(data)


# by t.me/yehuda100