"""
This module has some custom exceptions related to card
module.
"""

class CardException(Exception):
    """
    Base class for card exceptions
    """
    def __init__(self, message="Generic error with card module", *args, **kwargs):
        super().__init__(message, *args, **kwargs)
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
        super().__init__(message, *args, **kwargs)


class PaymentExceed(CardException):
    """
    raised when payment+free_limit exceed maximum card limit
    """
    def __init__(self, message="This payment exceeds maximum card limit", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class CardIsInactive(CardException):
    """
    raised when paying with inactive card
    """
    def __init__(self, message="This card is inactive", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


## Warnings


class CardWarning(Warning):
    """
    Base class for card warnings exceptions
    """
    def __init__(self, message="Generic warning with card module", *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.message = message


class CardActivationStateNotChanged(CardWarning):
    """
    raised when activation or deactivation don't change state,
    avoid changing in limits
    """
    def __init__(self, message="Activation state not changed", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class CardAlreadyInactive(CardActivationStateNotChanged):
    """
    Raised when card is already inactive
    """
    def __init__(self, message="Card already inactive", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class CardAlreadyActive(CardActivationStateNotChanged):
    """
    Raised when card is already active
    """
    def __init__(self, message="Card already active", *args, **kwargs):
        super().__init__(message, *args, **kwargs)