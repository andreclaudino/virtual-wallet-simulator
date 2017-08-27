
class PurchaseException(Exception):
    """
    Base class for purchase exceptions
    """
    def __init__(self, message="Generic error with purchase module", *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.message = message


class PurchaseUnchangeableProperty(PurchaseException):
    """
    Raised when changing a constant value in a purchase
    """
    def __init__(self, message="Can't change this purchase property", *args, **kwargs):
        super().__init__(message, *args, **kwargs)