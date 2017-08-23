class WalletException(Exception):
    """
    Base class for wallet exceptions
    """
    def __init__(self, message="Generic error with wallet module", *args, **kwargs):
        super(WalletException, self).__init__(message, *args, **kwargs)
        self.message = message


class WalletLimitExceed(WalletException):
    """
    raised when wallet's real limit exceed maximum limit
    """
    def __init__(self, message="Real Limit exceeds maximum permited", *args, **kwargs):
        super(WalletException, self).__init__(message, *args, **kwargs)
        self.message = message

class WalletLimitNotAllowed(WalletException):
    """
    raised when wallet limit is less than or equals to zero
    """
    def __init__(self, message="Changing Limit turns it less than or equals to zero", *args, **kwargs):
        super(WalletException, self).__init__(message, *args, **kwargs)
        self.message = message

class UnchangeableWalletValue(WalletException):
    """
    raised when trying to change an unchangeble wallet value
    """
    def __init__(self, message="This value can not be changed directly", *args, **kwargs):
        super(WalletException, self).__init__(message, *args, **kwargs)
        self.message = message