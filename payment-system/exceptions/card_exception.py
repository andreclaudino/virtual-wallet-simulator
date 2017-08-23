class CardException(Exception):
    """
    Base class for user exceptions
    """
    def __init__(self, message="Generic error with user module", *args, **kwargs):
        super(CardException, self).__init__(message, *args, **kwargs)
        self.message = message


# Exception raised when not all card parameters are given
class NotEnoughCardArguments(CardException):
    """
    Exception raised when trying to create
    an user without give an username
    """

    def __init__(self, *args, **kwargs):
        super().__init__('Not enought arguments given', *args, **kwargs)


class NotEnoughCardFreeLimit(CardException):
    """
    Exception raised when trying a purchase without
    enough free limit
    """
    def __init__(self, *args, **kwargs):
        super().__init__('Not enought free limit', *args, **kwargs)


class UnchangeableCardValue(CardException):
    """
    raised when trying to change an unchangeble card value
    """
    def __init__(self, message="This value can not be changed directly", *args, **kwargs):
        super(CardException, self).__init__(message, *args, **kwargs)