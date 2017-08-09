from unittest import TestCase

from base.connect_db import ConnectDB
from model.user import User, factors
import hashlib

class TestUser(TestCase):

    def setUp(self):
        ConnectDB.connect_database()

        self.pwd = 'v3ry_h@rd_p@$$w0rd'
        self.test = User(name="Testing User",
                    username="test01",
                    adress="0, Dummy Street, 219875-456",
                    phone_number='+55 21 99999-999',
                    mail_address='test@test_users.com',
                    password=self.pwd)
        self.test.save()

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

    def test_register_user_with_used_username(self):
        """
        Shouldn't save an user with an already
        used username
        """

        user2 = User(name="Testing User 02",
                     username="test01",
                     adress="0, Dummy Street, 219875-456",
                     phone_number='+55 21 99999-999',
                     mail_address='test@test_users.com',
                     password='weak password')

        user2.save()

        result = len(User.nodes.filter(username=self.test.username))
        self.assertEqual(1, result)

    def test_register_user_with_used_username_return_none(self):
        """
        Should get none when saving user with an already
        used username
        """
        user2 = User(name="Testing User 02",
                     username="test01",
                     password='weak password')

        result2 = user2.save()

        self.assertIsNone(result2, msg="Item was saved with same username")

    def test_update_user(self):
        """
        Update user means save an user with same username,
        but once is an uptade, not a register, should proceed
        """
        # Load the already created user
        user1 = User.nodes.get_or_none(username='test01')

        # update mail address:
        user1.mail_address = 'user1@mail_adress.com'

        # Try saving:
        result = user1.save()

        # Test if result is None (it is, if saving failed)
        self.assertIsNotNone(result)
        # Load again and test if e-mail was changed
        user2 = User.nodes.get_or_none(username='test01')
        self.assertEqual(user2.mail_address, 'user1@mail_adress.com')

    def test_login_correct_password(self):
        pass

    def test_login_incorrect_password(self):
        pass

    def tearDown(self):
        if self.test.save() is not None:
            self.test.delete()