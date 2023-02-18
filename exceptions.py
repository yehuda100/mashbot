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


class RequestException(MashBotExceptions):
    """
    handle all request related exceptions
    """
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

class JsonParseException(MashBotExceptions):
    """
    rasie if the program coud't get to the json data
    """
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

class UnreliableResponseException(MashBotExceptions):
    """
    raise an exception if the requsted date dos not match
    the response date.
    """
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)



#by t.me/yehuda100