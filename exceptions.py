class MashBotExceptions(Exception):
    """
    custom exseption class for MashBot
    """
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class DateFormattingException(MashBotExceptions):
    """
    custom exseption class for dates handling
    """
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

#by t.me/yehuda100