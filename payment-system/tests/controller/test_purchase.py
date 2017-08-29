from unittest.case import TestCase

from flask import json

from model.user import User
from utils.application_factory import create_app


class PurchaseTest(TestCase):
    """
    Tests for purchase and payment
    """

    def setUp(self):

        app = create_app()
        self.app = app.test_client()
        self.app.testing = True

        self.password = 'v3ry_h@rd_p@$$w0rd'
        self.username = 'test01'

        arguments = dict(name='Testing User',
                              username=self.username,
                              adress='0, Dummy Street, 219875-456',
                              phone_number='+55 21 99999-999',
                              mail_address='test@test_users.com',
                              password=self.password)

        self.app.post('/user', data=arguments, follow_redirects=True)

        result = self.app.post('/login', data=dict(username=self.username, password=self.password),
                               follow_redirects=True)
        data = json.loads(result.get_data(as_text=True))
        self.token = data['token']

        self.card_arguments = dict(number='00000000000000000000',
                                   expiration_date='11/18/2068',
                                   cvv='000')

        ## Add some cards to the wallet
        # Card 1
        self.app.post('/wallet/cards',
                      data={**self.card_arguments,
                            'due_day': 27,
                            'max_limit': 1000.0},
                      headers=dict(token=self.token), follow_redirects=True)

        # Card 2
        self.app.post('/wallet/cards',
                      data={**self.card_arguments,
                            'due_day': 12,
                            'max_limit': 2000.0},
                      headers=dict(token=self.token), follow_redirects=True)

        # Card 3
        self.app.post('/wallet/cards',
                      data={**self.card_arguments,
                            'due_day': 1,
                            'max_limit': 500.0},
                      headers=dict(token=self.token), follow_redirects=True)

    def tearDown(self):
        # Delete object
        user = User.nodes.get_or_none(username=self.username)
        if user:
            cards = user.wallets.single().cards

            for card in cards:
                card.delete()

            user.wallets.single().delete()
            user.delete()

    def test_purchase(self):
        """
        Purchase in a wallet
        """

        # First purchase
        value = 100.0
        # Do a purchase
        result = self.app.post('/wallet/purchase/{}'.format(value), headers=dict(token=self.token),
                               follow_redirects=True)
        purchase = json.loads(result.get_data(as_text=True))

        # Assert purchase value
        self.assertEqual(value, purchase['total'])

        # Second purchase
        value = 1300.0
        # Do a purchase
        result = self.app.post('/wallet/purchase/{}'.format(value), headers=dict(token=self.token),
                               follow_redirects=True)
        purchase = json.loads(result.get_data(as_text=True))

        # Assert purchase value
        self.assertEqual(value, purchase['total'])

    def test_pay_card(self):
        """
        pay an amount in card and get pay object
        """
        # Do a purchase
        value = 1300.0
        result = self.app.post('/wallet/purchase/{}'.format(value), headers=dict(token=self.token),
                               follow_redirects=True)
        purchase = json.loads(result.get_data(as_text=True))

        # Assert purchase value
        self.assertEqual(value, purchase['total'])

        # get one of used cards
        cid0 = purchase['relations']['cid']
        value0 = purchase['relations']['value']

        result = self.app.get('/wallet/cards/{}'.format(cid0), headers=dict(token=self.token),
                               follow_redirects=True)
        card0 = json.loads(result.get_data(as_text=True))

        # Test if card free limit was correct affected
        self.assertEqual(card0['free_limit'], card0['max_limit']-value)

        # Perform a payment
        payed_value = 50.0
        result = self.app.post('/wallet/cards/{cid}/pay'.format(cid=cid0),
                              data=dict(value=payed_value),
                              headers=dict(token=self.token),
                              follow_redirects=True)
        pay = json.loads(result.get_data(as_text=True))

        # get card updated
        result = self.app.get('/wallet/cards/{}'.format(cid0), headers=dict(token=self.token),
                              follow_redirects=True)
        card0 = json.loads(result.get_data(as_text=True))

        self.assertEqual(card0['free_limit'], card0['max_limit'] - value0 + payed_value)

