from neomodel.properties import StringProperty, EmailProperty
import math
import hashlib
from base.base_model import BaseModel

class User(BaseModel):
    # Basic field names
    name = StringProperty(required=True)
    username = StringProperty(required=True)
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
        suid = str(self.uid)
        a, b = factors(suid, value)
        s = zip(suid*a, value*b)
        p = ''.join([''.join(_) for _ in s]).encode('utf8')
        #TODO: Look for beter algorithm to use
        self.password_ = hashlib.sha384(p).hexdigest()
    
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
