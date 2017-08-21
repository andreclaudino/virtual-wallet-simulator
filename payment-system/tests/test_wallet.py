from unittest.case import TestCase

from base.connect_db import ConnectDB
from exceptions.wallet_exceptions import WalletLimitExceed, WalletLimitNotAllowed, UnchangebleWalletValue
from model.user import User
from model.wallet import Wallet


class TestWallet(TestCase):

    def setUp(self):
        ConnectDB.connect_database()
        self.user = User(name="Testing User 01",
                    username="test01",
                    adress="0, Dummy Street, 219875-456",
                    phone_number='+55 21 99999-999',
                    mail_address='test@test_users.com',
                    password='weak password')
        self.user.save()

        self.user.create_wallet("Test Wallet 01")

    def tearDown(self):
        self.user.wallets[0].delete()
        self.user.delete()

    def test_create_wallet_associated_with_user(self):
        """
        Create a Wallet in an User, then, test if it's correct
        associated
        """
        self.assertEqual(len(self.user.wallets), 1)

        wallet = Wallet.nodes.get_or_none(label="Test Wallet 01")

        self.assertEqual(self.user.wallets[0], wallet)

    def test_setting_real_limit_bigger_than_max_limit(self):
        """
        Raise WalletLimitExceed when real limit is bigger
        than max_limit
        """
        wallet = Wallet.nodes.get_or_none(label="Test Wallet 01")
        wallet.increase_max_limit(25.0)

        with self.assertRaises(WalletLimitExceed):
            wallet.real_limit = 30.0

    def test_decrease_of_max_limit(self):
        """
        Decreasing max limit should change real_limit
        if it's smaller than new value
        """

        wallet = self.user.wallets[0]
        wallet.increase_max_limit(25.0)
        wallet.real_limit = 20.0

        # decrease don't reach real_limit, should not affect
        wallet.decrease_max_limit(2.0)
        self.assertNotEqual(wallet.max_limit, wallet.real_limit)

        # decreace reaches real_limit, should affect
        wallet.decrease_max_limit(10.0)
        self.assertEqual(wallet.max_limit, wallet.real_limit)

    def test_raise_exception_if_max_limit_become_negative(self):
        """
        Should raise WalletLimitNotAllowed if max_limit become negative
        on decreasing
        """

        wallet = self.user.wallets[0]
        wallet.increase_max_limit(25.0)

        with self.assertRaises(WalletLimitNotAllowed):
            wallet.decrease_max_limit(30.0)

    def test_raise_exception_if_real_limit_become_negative(self):
        """
        Should raise WalletLimitNotAllowed if max_limit become negative
        on decreasing
        """

        wallet = self.user.wallets[0]

        with self.assertRaises(WalletLimitNotAllowed):
            wallet.real_limit = -1

    def test_raise_exception_on_changing_max_limit_directly(self):
        """
        Raise exception on changing "max_limit" directly
        """

        wallet = self.user.wallets[0]
        with self.assertRaises(UnchangebleWalletValue):
            wallet.max_limit = 10.0

