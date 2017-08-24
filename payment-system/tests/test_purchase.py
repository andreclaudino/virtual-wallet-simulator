from unittest.case import TestCase

from base.connect_db import ConnectDB


class TestPurchase(TestCase):
    def setUp(self):
        ConnectDB.connect_database()

    def tearDown(self):
        pass

    def test_purchasing_with_card(self):
        """
        Should reduce wallet free limit when payment is concluded
        """
        pass

    def test_purchasing_with_first_card(self):
        """
        Should purchase with the first card in order
        """
        pass

    def test_purchasing_with_other_card_then_first(self):
        """
        Should purchase with only a card, which is not the first
        """
        pass

    def test_purchasing_with_more_tan_one_card(self):
        """
        Should distribute purchasing with more than one card
        """
        pass

    def test_purchasing_without_enough_credit(self):
        """
        Should raise NotEnoughFreeLimit when purchasing
        without enough limit in wallet
        """
        pass
