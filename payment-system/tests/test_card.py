from unittest.case import TestCase

import datetime

from base.connect_db import ConnectDB
from exceptions.card_exception import NotEnoughCardArguments
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
            print("Due date is next month")
            self.assertEqual(card.due_date.month, month+1)

        # if due_day is not past this month, card due date is still this month
        if card.due_day > day:
            print("Due date is this month")
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
