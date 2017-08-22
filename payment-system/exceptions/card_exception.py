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