import hashlib
import math

from neomodel.properties import StringProperty, EmailProperty

from base.base_model import BaseModel
from exceptions.user_exception import UsernameInUse, UserInactive, UserPasswordNotGiven, UsernameNotGiven


class User(BaseModel):
    """
    This class models an user in database
    """
    # Basic field names
    name = StringProperty(required=True)
    username = StringProperty(required=True, unique_index=True)
    address = StringProperty(default=None)
    mail_address = EmailProperty(default=None)

    # Sensible data
    # TODO: Would be good hide password_ on collecting objetc
    password_ = StringProperty(db_property='password', required=True)

    @property
    def password(self):
        """
        Return hashed password
        :return: hashed password
        """
        return self.password_ if self.password_ else None

    @password.setter
    def password(self, value):
        """
        Once password need to be hashed, this method/property is
        used to hash entered password and save the hash instead
        of clean one
        """
        self.password_ = mixture_pwd(self.uid, value)

    def save(self):
        """
        validates if an username is in use before save it
        :return:
            * Saved user object if it's ok
            * 'username_in_use' if username already in use
            * 'no_password_given' if password is not set
            * 'no_username_given' if username is not set
        """
        if not hasattr(self, 'username') or self.username is None:
            raise UsernameNotGiven()

        if not hasattr(self, 'password_') or self.password_ is None:
            raise UserPasswordNotGiven()

        # validate username
        if len(User.nodes.filter(username=self.username, uid__ne=self.uid)) == 0:
            return super(User, self).save()
        else:
            # Found user with same username and different uid, so, username is in use
            raise UsernameInUse()

    @staticmethod
    def login(username, passwd):
        """
        Try to login an user
        :param username: username to login
        :param passwd: user password before hash
        :return:
            * True if login is ok,
            * False if wrong password
            * 'inexistent' if username not found
            * 'inactive' if user.active is False
        """
        # find user by username
        user = User.nodes.get_or_none(username=username)
        if user is None:
            return 'inexistent'
        hash_passwd = mixture_pwd(user.uid, passwd)
        if user.active:
            return (user.password_ == hash_passwd)
        else:
            raise UserInactive()


def factors(a_string,b_string):
    """
    Given two strings a and b, get the factors
    they should be multiplied to arrive same lenght
    :return minimum factors to arrive lcm for a, and b, in this order
    """
    # TODO: Beter docstring
    a = len(a_string)
    b = len(b_string)
    lcm =  int(abs(a * b) / math.gcd(a,b) if a and b else 0)
    return lcm // a, lcm // b


def mixture_pwd(base_k, val):
    """
    This function is used to mixture a value (used a password) with
    user id, then generate a hash who will be stored in database
    :param base_k: base key to mixture val
    :param val: value to be mixtured
    :return: hashstring of mixtured values
    """
    suid = str(base_k)
    value = str(val)
    a, b = factors(suid, value)
    s = zip(suid * a, value * b)
    p = ''.join([''.join(_) for _ in s]).encode('utf8')
    # TODO: Look for beter algorithm to use
    return hashlib.sha384(p).hexdigest()

