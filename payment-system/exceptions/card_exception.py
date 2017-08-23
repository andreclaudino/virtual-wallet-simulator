class CardException(Exception):
    """
    Base class for user exceptions
    """
    def __init__(self, message="Generic error with user module", *args, **kwargs):
        super(CardException, self).__init__(message, *args, **kwargs)
        self.message = message


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


class PaymentExceed(CardException):
    """
    raised when payment+free_limit exceed maximum card limit
    """
    def __init__(self, message="This payment exceeds maximum card limit", *args, **kwargs):
        super(CardException, self).__init__(message, *args, **kwargs)