from unittest import TestCase
from model.user import User, factors
import hashlib

class TestUser(TestCase):

    def setUp(self):
        self.pwd = 'v3ry_h@rd_p@$$w0rd'
        self.test = User(name="Testing User",
                    username="test01",
                    adress="0, Dummy Street, 219875-456",
                    phone_number='+55 21 99999-999',
                    mail_address='test@test_users.com',
                    password=self.pwd)

    def test_hashed_password(self):
        """
        Password should be hashed when set
        """
        suid = str(self.test.uid)
        a, b = factors(suid, self.pwd)
        s = zip(suid * a, self.pwd * b)
        p = ''.join([''.join(_) for _ in s]).encode('utf8')
        h = hashlib.sha384(p).hexdigest()

        self.assertEqual(h, self.test.password)

    def test_login_correct_password(self):
        pass

    def test_login_incorrect_password(self):
        pass

    def register_user_with_used_username(self):
        pass

