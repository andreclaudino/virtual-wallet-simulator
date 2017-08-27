"""
This module has some custom exceptions related to user module.
"""


class UserException(Exception):
    """
    Base class for user exceptions
    """
    def __init__(self, message="Generic error with user module", *args, **kwargs):
        super(UserException, self).__init__(message, *args, **kwargs)
        self.message = message


# Exceptions raised on saving user

class UsernameNotGiven(UserException):
    """
    Exception raised when trying to create
    an user without give an username
    """
    def __init__(self, *args, **kwargs):
        super().__init__('No username given', *args, **kwargs)


class UserPasswordNotGiven(UserException):
    """
    Exception raised when trying to create
    an user without give a password
    """
    def __init__(self, *args, **kwargs):
        super().__init__('No password given', *args, **kwargs)


class UsernameInUse(UserException):
    """
    Exception raised when choose username is already in use
    """
    def __init__(self, *args, **kwargs):
        super().__init__('Username already in use', *args, **kwargs)


# Exceptions raised on login

class UserPasswordIncorrect(UserException):
    """
    Raised in login, when user password is incorrect
    """
    def __init__(self, *args, **kwargs):
        super().__init__('Given password is incorrect', *args, **kwargs)


class UserInactive(UserException):
    """
    Raised when trying to login an inactive user
    """
    def __init__(self, *args, **kwargs):
        super().__init__('User is inactive', *args, **kwargs)


class UsernameNotFound(UserException):
    """
    Raised when trying to login an inexistent user
    """
    def __init__(self, *args, **kwargs):
        super().__init__('Username not found', *args, **kwargs)