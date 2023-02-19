from logger import logger


class MashBotExceptions(Exception):
    """
    custom exseption class for MashBot
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)
        logger.error(message, exc_info=False)


class DateFormattingException(MashBotExceptions):
    """
    custom exseption class for dates handling
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)


class UnreliableDataException(MashBotExceptions):
    """
    raise an exception if the requsted date dos not match
    the response date.
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)


class CBSException(MashBotExceptions):
    """
    raise an exception that somthing in the CBS process dosn't go as planned
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)
    #! this exception does not handled yet !#


#by t.me/yehuda100