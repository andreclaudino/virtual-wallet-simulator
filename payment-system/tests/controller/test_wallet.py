from unittest.case import TestCase

from flask import json
from functools import reduce

from model.user import User
from utils.application_factory import create_app


class WalletTest(TestCase):

    def setUp(self):

        app = create_app()
        self.app = app.test_client()
        self.app.testing = True

        self.password = 'v3ry_h@rd_p@$$w0rd'
        self.username = 'test01'

        arguments = dict(name='Testing User',
                              username=self.username,
                              address='0, Dummy Street, 219875-456',
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

    def tearDown(self):
        # Delete object
        user = User.nodes.get_or_none(username=self.username)
        if user:
            user.wallets.single().delete()
            user.delete()

    def test_get_wallet_information(self):
        """
        Get wallet information, set limit, add card,
        and get information again
        """
        result = self.app.get('/wallet', headers=dict(token=self.token), follow_redirects=True)

        wallet = json.loads(result.get_data(as_text=True))

        # Test presence of all wallet attributes
        self.assertIn('real_limit', wallet)
        self.assertIn('max_limit', wallet)
        self.assertIn('free_limit', wallet)
        self.assertIn('real_free_limit', wallet)
        self.assertIn('total_used', wallet)
        self.assertIn('total_cards', wallet)

    def test_set_real_limit(self):
        """
        Set real limit and test if it was changed
        """
        ## Create a card
        self.app.post('/wallet/cards',
                      data={**self.card_arguments,
                            'due_day': 27,
                            'max_limit': 1000.0},
                      headers=dict(token=self.token), follow_redirects=True)

        # set real limit
        result = self.app.put('/wallet/real_limit/{}'.format(500.0), headers=dict(token=self.token),
                              follow_redirects=True)
        self.assertEqual(result.status_code, 200)

        # Get wallet information and test free limit
        result = self.app.get('/wallet', headers=dict(token=self.token), follow_redirects=True)
        wallet = json.loads(result.get_data(as_text=True))

        self.assertEqual(wallet['real_limit'], 500.0)

    def test_manage_of_cards_in_a_wallet(self):
        """
        Manage inserting, deactivating and fetching cards

        * Add some cards
        * Assert inserted cards

        * Remove some cards
        * Assert removed (deactivate) cards
        """
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

        # Get list of cards
        result = self.app.get('/wallet/cards', headers=dict(token=self.token), follow_redirects=True)
        data = json.loads(result.get_data(as_text=True))
        cards = data['cards']

        # Sum cards limits
        max_limit = reduce(lambda c1, c2: c1 + c2['max_limit'], cards, 0)

        # Get wallet information
        result = self.app.get('/wallet', headers=dict(token=self.token), follow_redirects=True)
        wallet = json.loads(result.get_data(as_text=True))

        # Compare wallet max limit with the sum of cards max_limits
        self.assertEqual(max_limit, wallet['max_limit'])

        # deactivate a card
        card0 = cards[0]
        self.app.delete('/wallet/cards/{}'.format(card0['uid']), headers=dict(token=self.token),
                        follow_redirects=True)

        # Test new card list
        result = self.app.get('/wallet/cards', headers=dict(token=self.token), follow_redirects=True)
        data = json.loads(result.get_data(as_text=True))
        card0 = data['cards'][0]

        # Assert card0 is deactivated
        self.assertFalse(card0['active'])

