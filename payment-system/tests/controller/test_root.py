from unittest.case import TestCase

from flask import json

from base.connect_db import ConnectDB
from exceptions.user_exceptions import UserPasswordIncorrect, UsernameNotFound, UserInactive
from model.user import User
from utils.application_factory import create_app


class RootTest(TestCase):

    def setUp(self):
        ConnectDB.connect_database()
        app = create_app()
        self.app = app.test_client()
        self.app.testing = True

        self.password = 'v3ry_h@rd_p@$$w0rd'
        self.username = 'test01'

        self.arguments = dict(name='Testing User',
                         username=self.username,
                         address='0, Dummy Street, 219875-456',
                         phone_number='+55 21 99999-999',
                         mail_address='test@test_users.com',
                         password=self.password)

        # Create test user
        result = self.app.post('/user', data=self.arguments, follow_redirects=True)
        self.data = json.loads(result.get_data(as_text=True))

        self.uid = self.data['uid']

    def tearDown(self):
        # Delete object
        user = User.nodes.get_or_none(username=self.username)
        if user:
            user.delete()

    def test_login_correct(self):
        """
        Test if login with correct credentials return
        username and token
        """

        # Perform login
        result = self.app.post('/login',
                               data=dict(username=self.username, password=self.password),
                               follow_redirects=True)
        data = json.loads(result.get_data(as_text=True))
        
        # Test login
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['user']['username'], self.username)
        self.assertEqual(data['user']['uid'], self.uid)
        self.assertIsNotNone(data['token'])

    def test_login_incorrect_password(self):
        """
        Should return 401 on incorrect password
        and match UserPasswordIncorrect message
        """
        # Perform login
        result = self.app.post('/login',
                               data=dict(username=self.username, password='wrong_password'),
                               follow_redirects=True)
        data = json.loads(result.get_data(as_text=True))

        # Test login
        self.assertEqual(result.status_code, 401)
        self.assertEqual(data['error'], str(UserPasswordIncorrect()))

    def test_login_not_found_username(self):
        """
        Should return 401 on incorrect username
        and match UsernameNotFound message
        """
        # Perform login
        result = self.app.post('/login',
                               data=dict(username='wrong_username', password=self.password),
                               follow_redirects=True)
        data = json.loads(result.get_data(as_text=True))

        # Test login
        self.assertEqual(result.status_code, 401)
        self.assertEqual(data['error'], str(UsernameNotFound()))

    def test_login_inactive_user(self):
        """
        Should return 401 on login_in inactive
        user and match UserInactive message
        """

        # Make user inactive
        user = User.nodes.get_or_none(uid=self.uid)
        user.active = False
        user.save()

        # Perform login
        result = self.app.post('/login',
                               data=dict(username=self.username, password=self.password),
                               follow_redirects=True)
        data = json.loads(result.get_data(as_text=True))

        # Test login
        self.assertEqual(result.status_code, 401)
        self.assertEqual(data['error'], str(UserInactive()))

    def test_verify_token(self):
        """
        Should return information about a token:
        username, user id (uid), and wallet id
        (wid), because token is valid
        """

        # Login user and get token
        result = self.app.post('/login',
                               data=dict(username=self.username, password=self.password),
                               follow_redirects=True)

        data = json.loads(result.get_data(as_text=True))
        username = data['user']['username']
        uid = data['user']['uid']
        wid = data['user']['wid']
        token = data['token']

        result = self.app.get('/whoami', headers=dict(token=token), follow_redirects=True)
        data = json.loads(result.get_data(as_text=True))

        self.assertEqual(username, data['username'])
        self.assertEqual(uid, data['uid'])
        self.assertEqual(wid, data['wid'])

    def test_verify_incorrect_token(self):
        """
        Should fail because token is invalid
        """

        # Login user and get token
        result = self.app.post('/login',
                               data=dict(username=self.username, password=self.password),
                               follow_redirects=True)

        data = json.loads(result.get_data(as_text=True))
        token = data['token']

        result = self.app.get('/whoami', headers=dict(token='000000'), follow_redirects=True)

        self.assertEqual(result.status_code, 401)
