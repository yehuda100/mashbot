from math import ceil
from datetime import datetime
from typing import Optional
from dateutil.relativedelta import relativedelta
import mongodb as db
import interest as inst


class ConstructionData():
    """
    class to represent the home owner and
    calculate all the payments and interest attached.
    """
    def __init__(self, user_id: int, name: str, permit_date: datetime, signing_date: datetime,\
        price: int, amount_payed: Optional[int]= 0, finish_date: Optional[datetime]= datetime(2026, 6, 30),) -> None:

        # Constructor function to initialize the instance variables of the class
        self.user_id: int = user_id
        self.name: str = name
        self.permit_date: datetime = permit_date
        self.signing_date:datetime = signing_date
        self.price: int = price
        self.amount_payed: int = amount_payed
        self.finish_date:datetime = finish_date


    #! the assumption is the GESHEM payment board!
    @property
    def pay_dates(self) -> dict: 
        # A property function to calculate and return a dictionary of payment dates for each payment number
        # based on the assumption of GESHEM payment board
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
        # A property function to return a dictionary of percentage of total price to be paid for each payment number
        # The percentages are hardcoded and don't change based on any external factors
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
        # A property function to calculate and return the total amount to be paid for all the payments
        # up to the next payment date based on the percentage of total price to be paid for each payment number
        next_payment = self.get_next_payment_number()
        percentage_to_be_payd = sum(v for k, v in self.pay_percentage.items() if k < next_payment)
        return self.price * percentage_to_be_payd


    def next_payment(self) -> dict:
        """
        Calculates the details of the next payment to be made for the construction project.

        Returns:
        dict: A dictionary containing the payment number, payment amount, and payment date.
        """
        payment_number = self.__get_next_payment_number()
        payment_amount = self.__get_next_payment_amount(payment_number)
        result = {
            "payment_number": payment_number,
            "payment_amount": payment_amount,
            "payment_date": self.pay_dates[payment_number]
        }
        return result

    async def save(self) -> None:
        """
        Saves the construction data to the database.
        """
        data = self.__dict__
        db.save_construction_data(data)


    def __get_next_payment_number(self) -> int:
        """
        Finds the next payment number for the construction project.

        Returns:
        int: The next payment number.
        """
        for payment_number, date in self.pay_dates.items():
            if datetime.today() < date:
                return payment_number

    def __get_next_payment_amount(self, payment_number: int) -> int:
            """
            Calculates the amount to be paid for the next payment.

            Args:
            payment_number (int): The payment number for which the amount needs to be calculated.

            Returns:
            int: The amount to be paid for the next payment.
            """
            if self.amount_payed >= self.amount_to_be_payd:
                return 0
            amount: float = self.price * self.pay_percentage[payment_number]
            if payment_number in (1, 2):
                return ceil(amount)
            interest: float = amount * (inst.get_interest_from_date(self.permit_date) / 100)
            return ceil(amount + interest / 2)


# by t.me/yehuda100