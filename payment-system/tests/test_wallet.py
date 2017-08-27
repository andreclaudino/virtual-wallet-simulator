from unittest.case import TestCase

from base.connect_db import ConnectDB
from exceptions.wallet_exceptions import WalletLimitExceed
from exceptions.wallet_exceptions import WalletLimitNotAllowed
from exceptions.wallet_exceptions import UnchangeableWalletValue
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

        self.wallet = self.user.create_wallet("Test Wallet 01")
        self.wallet_uid = self.user.wallets[0].uid

    def tearDown(self):
        self.wallet.delete()
        self.user.delete()

    def test_create_wallet_associated_with_user(self):
        """
        Create a Wallet in an User, then, test if it's correct
        associated
        """
        wallet = Wallet.nodes.get_or_none(uid=self.wallet_uid)
        self.assertEqual(self.user.wallets[0], wallet)

    def test_setting_real_limit_bigger_than_max_limit(self):
        """
        Raise WalletLimitExceed when real limit is bigger
        than max_limit
        """
        wallet = Wallet.nodes.get_or_none(uid=self.wallet_uid)
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
        with self.assertRaises(UnchangeableWalletValue):
            wallet.max_limit = 10.0

    def test_wallet_max_limit_increase_on_card_creation(self):
        """
        Wallet max limit should be increased on card creation
        by card's max_limit
        """

        limit_before = self.wallet.max_limit
        self.card = self.wallet.create_card(number='4539707916792445',
                                            due_day=15,
                                            expiration_date='05/25/2022',
                                            cvv='453',
                                            max_limit=300.0)
        limit_after = self.wallet.max_limit
        self.assertEqual(limit_after, limit_before+300.0)

        self.card.delete()

    def test_wallet_free_limit_increase_on_card_creation(self):
        """
        Wallet free limit should be increased on card creation
        by card's free_limit
        """
        limit_before = self.wallet.free_limit
        self.card = self.wallet.create_card(number='4539707916792445',
                                            due_day=15,
                                            expiration_date='05/25/2022',
                                            cvv='453',
                                            max_limit=300.0)
        limit_after = self.wallet.free_limit
        self.assertEqual(limit_after, limit_before + 300.0)

        self.card.delete()

    def test_ignoring_deactivated_cards_on_sort(self):
        """
        Should remove deactivated cards on card sorting
        """
        [_.delete() for _ in self.wallet.cards]

        card2 = self.wallet.create_card(number='4539707916792445',
                                        due_day=15,
                                        expiration_date='05/25/2022',
                                        cvv='002',
                                        max_limit=300.0)
        card1 = self.wallet.create_card(number='4539707916792445',
                                        due_day=20,
                                        expiration_date='05/25/2022',
                                        cvv='001',
                                        max_limit=300.0)
        card1.active = False
        card1.save()

        card3_3 = self.wallet.create_card(number='4539707916792445',
                                          due_day=13,
                                          expiration_date='05/25/2022',
                                          cvv='005',
                                          max_limit=700.0)
        card3_1 = self.wallet.create_card(number='4539707916792445',
                                          due_day=13,
                                          expiration_date='05/25/2022',
                                          cvv='003',
                                          max_limit=200.0)
        card3_2 = self.wallet.create_card(number='4539707916792445',
                                          due_day=13,
                                          expiration_date='05/25/2022',
                                          cvv='004',
                                          max_limit=500.0)
        card3_2.active = False
        card3_2.save()

        card4 = self.wallet.create_card(number='4539707916792445',
                                        due_day=10,
                                        expiration_date='05/25/2022',
                                        cvv='006',
                                        max_limit=300.0)

        card5_1 = self.wallet.create_card(number='4539707916792445',
                                          due_day=3,
                                          expiration_date='05/25/2022',
                                          cvv='007',
                                          max_limit=200.0)
        card5_2 = self.wallet.create_card(number='4539707916792445',
                                          due_day=3,
                                          expiration_date='05/25/2022',
                                          cvv='008',
                                          max_limit=300.0)

        for _ in self.wallet.cards:
            _.set_fake_today(fake_today='08/22/2017')

        self.assertListEqual(self.wallet.sorted_cards(), [card2, card3_1, card3_3, card4, card5_1,
                                                          card5_2])

    def test_free_limit_setting_directly(self):
        """
        Should raise an UnchangeableWalletValue exception
        when changing free_limit directly
        """
        with self.assertRaises(UnchangeableWalletValue):
            self.user.wallets[0].free_limit = 100.0

    def test_free_limit_negative(self):
        """
        Should raise WalletLimitNotAllowed when free_limit
        become negative
        """
        with self.assertRaises(WalletLimitNotAllowed):
            self.user.wallets[0].decrease_free_limit(1000)
