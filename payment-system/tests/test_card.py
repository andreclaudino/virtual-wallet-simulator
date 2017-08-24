from unittest.case import TestCase

import datetime

from base.connect_db import ConnectDB
from exceptions.card_exception import NotEnoughCardArguments, CardAlreadyInactive, CardAlreadyActive, CardIsInactive
from exceptions.card_exception import NotEnoughCardFreeLimit
from exceptions.card_exception import UnchangeableCardValue
from exceptions.card_exception import PaymentExceed
from model.card import Card
from model.user import User
from datetime import datetime


class TestCard(TestCase):

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
        self.wallet = self.user.wallets[0]

        self.card = self.wallet.create_card(number='4539707916792445',
                                            due_day= 15,
                                            expiration_date='05/25/2022',
                                            cvv='453',
                                            max_limit=300.0)

    def tearDown(self):
        self.card.delete()
        self.wallet.delete()
        self.user.delete()

    def test_create_card_without_required_fields(self):
        """
        Should return NotEnoughCardArguments when there is not
        all default parameters
        """

        with self.assertRaises(NotEnoughCardArguments):
            self.wallet.create_card()

    def test_card_connection_to_wallet(self):
        """
        created card should be conected to wallet
        """
        uid = self.card.uid

        card = Card.nodes.get_or_none(uid=uid)

        # Card should be found in database
        self.assertIsNotNone(card)
        # Card taken from database and created should be the same
        self.assertEqual(card, self.card)
        # Card taken from wallet conection and from database should be the same
        self.assertEqual(card, self.wallet.cards[0])

    def test_due_day_from_1_to_28(self):
        """
        To avoid problems with some months, due_day should
        be from 1 to 28, this way, february (with 28 or 29 days)
        and other months (with 30, not 31 days) will not have
        problems
        """
        with self.assertRaises(ValueError):
            self.wallet.create_card(number='4539707916792445',
                                    due_day=29,
                                    expiration_date='05/25/2022',
                                    cvv='453',
                                    max_limit=300.0)

    def test_due_date(self):
        """
        Due date should be in this month if due day is not
        past, but should be next month if day is passed
        """

        day = datetime.today().day
        month = datetime.today().month

        # Set due_day as today-1, due_date should be next month
        card = self.wallet.create_card(number='5537071187522237',
                                due_day=22,
                                expiration_date='05/25/2022',
                                cvv='453',
                                max_limit=300.0)

        # if due_day is past this month (due_day is less than today's day), card due date is next month
        if card.due_day <= day:
            self.assertEqual(card.due_date.month, month+1)

        # if due_day is not past this month, card due date is still this month
        if card.due_day > day:
            self.assertEqual(card.due_date.month, month)

        card.delete()

    def test_sorting_cards_all_next_month(self):
        """
        Cards should be sorted firts descendently by due date,
        next ascendently by limit
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

        self.assertListEqual(self.wallet.sorted_cards(), [card1, card2, card3_1, card3_2, card3_3, card4, card5_1,
                                                          card5_2])

        for _ in self.wallet.cards:
            _.delete()

    def test_sorting_cards_some_this_month(self):
        """
        Cards should be sorted firts descendently by due date,
        next ascendently by limit
        """

        [_.delete() for _ in self.wallet.cards]

        card2 = self.wallet.create_card(number='4539707916792445',
                                        due_day=28,
                                        expiration_date='05/25/2022',
                                        cvv='002',
                                        max_limit=300.0)
        card1 = self.wallet.create_card(number='4539707916792445',
                                        due_day=20,
                                        expiration_date='05/25/2022',
                                        cvv='001',
                                        max_limit=300.0)

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
                                          due_day=25,
                                          expiration_date='05/25/2022',
                                          cvv='004',
                                          max_limit=500.0)

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

        self.assertListEqual(self.wallet.sorted_cards(), [card1, card3_1, card3_3, card4, card5_1,
                                                          card5_2, card2, card3_2])

        for _ in self.wallet.cards:
            _.delete()

    def test_raise_exception_on_change_free_limit_directly(self):
        """
        Should raise an exception when free_limit is
        changed directly
        """
        with self.assertRaises(UnchangeableCardValue):
            self.card.free_limit = 500.0

    def test_purchasing(self):
        """
        Should reduce card free limit when payment is concluded
        """
        before_limit = self.card.free_limit
        self.card.purchase(200.0)
        after_limit = self.card.free_limit

        self.assertEqual(before_limit-200, after_limit)

    def test_purchasing_without_enough_limit(self):
        """
        Should raise NotEnoughCardFreeLimit
        if card has not enough free limit during
        purchase
        """
        before_limit = self.card.free_limit

        with self.assertRaises(NotEnoughCardFreeLimit):
            self.card.purchase(before_limit+100.0)

    def test_releasing_credit(self):
        """
        Should increase free limit by releasing credit, same for
        wallet limit
        """

        before_limit = self.card.free_limit
        self.card.purchase(200.0)
        self.card.pay(100.0)
        after_limit = self.card.free_limit
        self.assertEqual(before_limit - 100.0, after_limit)

    def test_raise_exception_on_exceed_payment(self):
        """
        Should raise PaymentExceed when
        value+card.free_limit exceed card maximum limit
        """
        self.card.purchase(200.0)

        with self.assertRaises(PaymentExceed):
            self.card.pay(300.0)

    def test_deactivating_inactive_card(self):
        """
        Should raise exception when card is already
        inactive
        """
        # Raise exception if removing an already removed card
        self.card.active = False
        self.card.save()
        with self.assertWarns(CardAlreadyInactive):
            self.card.active = False

    def test_activating_active_card(self):
        """
        Should raise exception when card is already
        inactive
        """
        # Raise exception if removing an already removed card
        with self.assertWarns(CardAlreadyActive):
            self.card.active = True

    def test_wallets_max_limit_increase_on_card_activation(self):
        """
        Wallet max limit should be increased on activating card
        """
        card = self.wallet.create_card(number='4539707916792445',
                                       due_day=15,
                                       expiration_date='05/25/2022',
                                       cvv='453',
                                       max_limit=100.0)

        ## Get limit with new card
        limit_before = self.wallet.max_limit

        # deactivate card, limit will be reduced
        card.active = False
        self.wallet.refresh()
        limit_after = self.wallet.max_limit

        self.assertEqual(limit_after, limit_before - card.max_limit)

        # Activate card again, limit should be increased
        card.active = True
        self.wallet.refresh()
        limit_after = self.wallet.max_limit

        self.wallet.refresh()
        self.assertEqual(limit_after, limit_before)

        card.delete()

    def test_wallets_max_limit_reduction_on_card_deactivation(self):
        """
        Wallet max limit should be decreased on deactivating card
        """
        card = self.wallet.create_card(number='4539707916792445',
                                       due_day=15,
                                       expiration_date='05/25/2022',
                                       cvv='453',
                                       max_limit=100.0)

        limit_before = self.wallet.max_limit
        card.active = False
        self.wallet.refresh()
        limit_after = self.wallet.max_limit

        self.assertEqual(limit_after, limit_before-card.max_limit)

        card.delete()

    def test_wallets_free_limit_increase_on_card_activation(self):
        """
        Wallet free limit should be increased on activating card
        """
        card = self.wallet.create_card(number='4539707916792445',
                                       due_day=15,
                                       expiration_date='05/25/2022',
                                       cvv='453',
                                       max_limit=100.0)

        ## Get limit with new card
        limit_before = self.wallet.free_limit

        # deactivate card, limit will be reduced
        card.active = False
        self.wallet.refresh()
        limit_after = self.wallet.free_limit

        self.assertEqual(limit_after, limit_before - card.free_limit)

        # Activate card again, limit should be increased
        card.active = True
        self.wallet.refresh()
        limit_after = self.wallet.free_limit

        self.wallet.refresh()
        self.assertEqual(limit_after, limit_before)

        card.delete()

    def test_wallets_free_limit_reduction_on_card_deactivation(self):
        """
        Wallet free limit should be decreased on deactivating card
        """
        card = self.wallet.create_card(number='4539707916792445',
                                       due_day=15,
                                       expiration_date='05/25/2022',
                                       cvv='453',
                                       max_limit=100.0)

        limit_before = self.wallet.free_limit
        card.active = False
        self.wallet.refresh()
        limit_after = self.wallet.free_limit

        self.assertEqual(limit_after, limit_before - card.free_limit)

        card.delete()

    def test_wallet_free_limit_reduction_on_card_purchase(self):
        limit_before = self.wallet.free_limit
        self.wallet.cards[0].purchase(100.0)
        self.wallet.refresh()

        limit_after = self.wallet.free_limit
        self.assertEqual(limit_after, limit_before-100.0)

    def test_wallet_free_limit_increase_on_card_payment(self):
        """
        Should increase wallet free_limit on card payment
        """
        limit_before = self.wallet.free_limit

        # purchase 100 to reduce limit
        self.wallet.cards[0].purchase(100.0)

        # refresh
        self.wallet.refresh()

        limit_after = self.wallet.free_limit
        self.assertEqual(limit_after, limit_before - 100.0)

        # pay 50.0
        self.wallet.cards[0].pay(50.0)
        self.wallet.cards[0].refresh()

        # refresh
        self.wallet.refresh()

        limit_after = self.wallet.free_limit

        self.assertEqual(limit_after, limit_before - 50.0)

    def test_purchasing_with_inactive_card(self):
        """
        Should raise CardIsInactive when purchasing
        with inactive card
        """
        self.card.active = False
        self.card.save()

        with self.assertRaises(CardIsInactive):
            self.card.purchase(100.0)

    def test_bill_generation(self):
        pass