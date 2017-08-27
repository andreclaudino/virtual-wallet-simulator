from unittest.case import TestCase

from base.connect_db import ConnectDB
from exceptions.card_exceptions import PaymentExceed
from model.user import User


class TestPurchase(TestCase):

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

        self.card = self.wallet.create_card(number='4539707916792445',
                                            due_day=15,
                                            expiration_date='05/25/2022',
                                            cvv='453',
                                            max_limit=300.0)

        self.purchase = self.wallet.purchase(100.0)
        self.card.refresh()
        self.wallet.refresh()

    def tearDown(self):
        self.purchase.delete()
        self.card.delete()
        self.wallet.delete()
        self.user.delete()

    def test_payment_exceed_card_limit(self):
        """
        When paying, raise PaymentExceed if it's
        exceeding card max limit.
        """
        with self.assertRaises(PaymentExceed):
            self.card.pay(200.0)

    def test_payment_should_increase_free_limit_of_card(self):
        """
        On paying card, it should increase it's free_limit
        """
        before_limit = self.card.free_limit
        payment = self.card.pay(50.0)
        after_limit = self.card.free_limit

        self.assertEqual(after_limit, before_limit+50.0)

        payment.delete()

    def test_payment_should_increase_free_limit_of_wallet(self):
        """
        On paying card, it should increase
        wallet free_limit
        """
        before_limit = self.wallet.free_limit
        payment = self.card.pay(50.0)
        self.wallet.refresh()
        after_limit = self.wallet.free_limit

        self.assertEqual(after_limit, before_limit + 50.0)

        payment.delete()

    def test_connecting_payment_to_card(self):
        """
        On Paying, it should
        connect Payment object to card
        """
        payment = self.card.pay(80)

        self.card.refresh()
        self.assertIn(payment, self.card.payments)
        self.assertEqual(payment.card.single(), self.card)

        payment.delete()

    def test_connecting_payment_to_wallet(self):
        """
        On Paying, it should
        connect Payment object to wallet
        """
        payment = self.card.pay(80)

        self.wallet.refresh()

        self.assertIn(payment, self.wallet.payments)
        self.assertEqual(payment.wallet.single(), self.wallet)

        payment.delete()
