from unittest.case import TestCase

from base.connect_db import ConnectDB
from exceptions.wallet_exceptions import RealLimitExceeded
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

    def tearDown(self):
        self.card.delete()
        self.wallet.delete()
        self.user.delete()

    def test_connecting_purchase_to_wallet_on_create(self):
        """
        On creating a Purchase object, it should
        connect to wallet, and wallet, should
        be connected to it
        """
        # Do a purchase
        purchase = self.wallet.purchase(100.0)

        # verify if a purchase is connected with wallet in both directions
        self.assertEqual(purchase, self.wallet.purchases[0])
        self.assertEqual(purchase.wallet.single, self.wallet)

    def test_connecting_purchase_to_wallet_on_create(self):
        """
        On creating a Purchase object, it should
        connect to card, and card, should
        be connected to it
        """
        # Do a purchase
        purchase = self.wallet.purchase(100.0)

        # verify if a purchase is connected with card in both directions
        self.assertEqual(purchase, self.wallet.cards[0].purchases[0])
        self.assertEqual(purchase.cards[0], self.wallet.cards[0])

    def test_purchase_should_reduce_free_limit_of_wallet(self):
        """
        On creating a Purchase object, should reduce
        wallet free_limit
        """
        limit_before = self.wallet.free_limit
        self.wallet.purchase(100.0)
        self.wallet.refresh()

        limit_after = self.wallet.free_limit

        self.assertEqual(limit_after, limit_before-100.0)

    def test_purchase_should_reduce_free_limit_of_card(self):
        """
        On creating a Purchase object, should reduce
        credit card free_limit
        """
        limit_before = self.card.free_limit
        self.wallet.purchase(100.0)
        self.card.refresh()

        limit_after = self.card.free_limit

        self.assertEqual(limit_after, limit_before-100.0)

    def test_purchasing_with_other_card_then_first(self):
        """
        Should purchase with only one card, which is not the first,
        free_limits and purchase connections should be correct
        """
        card2 = self.wallet.create_card(number='4539707916792445',
                                        due_day=13,
                                        expiration_date='05/25/2022',
                                        cvv='453',
                                        max_limit=500.0)

        purchase = self.wallet.purchase(400)

        self.assertIn(card2, purchase.cards)
        self.assertNotIn(self.card, purchase.cards)

        rel = purchase.cards.relationship(card2)
        self.assertEqual(rel.value, 400)

    def test_connections_when_purchasing_with_more_tan_one_card(self):
        """
        Should connect purchase to each card which was used
        """
        card2 = self.wallet.create_card(number='4539707916792445',
                                due_day=13,
                                expiration_date='05/25/2022',
                                cvv='453',
                                max_limit=200.0)

        card3 = self.wallet.create_card(number='4539707916792445',
                                            due_day=11,
                                            expiration_date='05/25/2022',
                                            cvv='453',
                                            max_limit=100.0)

        card4 = self.wallet.create_card(number='4539707916792445',
                                        due_day=11,
                                        expiration_date='05/25/2022',
                                        cvv='453',
                                        max_limit=200.0)

        # Should use self.card, card2 and card3 and ignore card4
        purchase = self.wallet.purchase(550.0)

        self.assertIn(self.card, purchase.cards)
        self.assertIn(card2, purchase.cards)
        self.assertIn(card3, purchase.cards)
        self.assertNotIn(card4, purchase.cards)

    def test_values_used_when_purchasing_with_more_tan_one_card(self):
        """
        Should distribute values on each card according to card sorting

        Amount should be:
        * 300 in self.card
        * 200 in card2
        * 50 in card3
        """
        card2 = self.wallet.create_card(number='4539707916792445',
                                        due_day=13,
                                        expiration_date='05/25/2022',
                                        cvv='453',
                                        max_limit=200.0)

        card3 = self.wallet.create_card(number='4539707916792445',
                                        due_day=11,
                                        expiration_date='05/25/2022',
                                        cvv='453',
                                        max_limit=100.0)

        card4 = self.wallet.create_card(number='4539707916792445',
                                        due_day=11,
                                        expiration_date='05/25/2022',
                                        cvv='453',
                                        max_limit=200.0)

        # Should use self.card, card2 and card3 and ignore card4
        purchase = self.wallet.purchase(550.0)

        rel = purchase.cards.relationship(self.card)
        self.assertEqual(rel.value, 300)

        rel = purchase.cards.relationship(card2)
        self.assertEqual(rel.value, 200)

        rel = purchase.cards.relationship(card3)
        self.assertEqual(rel.value, 50)

    def test_purchasing_without_enough_credit(self):
        """
        Should raise RealLimitExceeded when purchasing
        without enough limit in wallet
        """
        with self.assertRaises(RealLimitExceeded):
            self.wallet.purchase(5000.0)
