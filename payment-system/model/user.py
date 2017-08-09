from neomodel.properties import StringProperty, EmailProperty
import math
import hashlib
from base.base_model import BaseModel

class User(BaseModel):
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
        return self.password_ if self.password_ else None

    @password.setter
    def password(self, value):
        self.password_ = hash_pwd(self.uid, value)

    def save(self):
        # validate username
        if len(User.nodes.filter(username=self.username, uid__ne=self.uid)) == 0:
            return super(User, self).save()
        else:
            return None

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
        hash_passwd = hash_pwd(user.uid, passwd)
        return (user.password_ == hash_passwd) if user.active else 'inactive'

def factors(a_string,b_string):
    """
    Given two numbers a, b, get the factors
    they should be multiplied to arrive
    common multiple
    """
    # TODO: Beter docstring
    a = len(a_string)
    b = len(b_string)
    lcm =  int(abs(a * b) / math.gcd(a,b) if a and b else 0)
    return lcm // a, lcm // b

def hash_pwd(base_k, val):
    suid = str(base_k)
    value = str(val)
    a, b = factors(suid, value)
    s = zip(suid * a, value * b)
    p = ''.join([''.join(_) for _ in s]).encode('utf8')
    # TODO: Look for beter algorithm to use
    return hashlib.sha384(p).hexdigest()
