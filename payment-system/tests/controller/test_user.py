from unittest.case import TestCase

from flask import json

from base.connect_db import ConnectDB
from model.user import User
from utils.application_factory import create_app


class UserTest(TestCase):

    def setUp(self):
        ConnectDB.connect_database()
        app = create_app()
        self.app = app.test_client()
        self.app.testing = True

        self.password = 'v3ry_h@rd_p@$$w0rd'
        self.username = 'test01'

        self.arguments = dict(name='Testing User',
                              username=self.username,
                              adress='0, Dummy Street, 219875-456',
                              phone_number='+55 21 99999-999',
                              mail_address='test@test_users.com',
                              password=self.password)

    def tearDown(self):
        # Delete object
        user = User.nodes.get_or_none(username=self.username)
        if user:
            user.delete()

    def test_create_user(self):
        """
        Should create an user in database
        """

        result = self.app.post('/user', data=self.arguments, follow_redirects=True)

        ## Check http created status
        self.assertEqual(result.status_code, 201)

        ## Check attributes from user object
        user = User.nodes.get_or_none(username='test01')
        self.assertIsNotNone(user)
        self.assertEqual(user.name, self.arguments['name'])
        self.assertEqual(user.username, self.arguments['username'])
        self.assertIsNotNone(user.uid)
        self.assertTrue(user.active)

    def test_create_user_with_used_username(self):
        """
        Should raise UsernameInUse when creating
        user with an already used username
        """
        # First creation should be ok returning created status (201)
        result = self.app.post('/user', data=self.arguments, follow_redirects=True)
        self.assertEqual(result.status_code, 201)

        # Second creation should return a conflict status (409)
        result = self.app.post('/user', data=self.arguments, follow_redirects=True)
        data = json.loads(result.get_data(as_text=True))

        self.assertEqual(result.status_code, 409)
        self.assertEqual(data['error'], 'Username already in use')

    def test_get_user_by_uuid(self):
        """
        Should get an user by uid
        """
        # First creation should be ok returning created status (201)
        result = self.app.post('/user', data=self.arguments, follow_redirects=True)

        self.assertEqual(result.status_code, 201)
        data = json.loads(result.get_data(as_text=True))
        uid = data['uid']

        result = self.app.post('/login', data=dict(username=self.username, password=self.password),
                      follow_redirects=True)
        data = json.loads(result.get_data(as_text=True))
        token = data['token']

        result = self.app.get('/user/{}'.format(uid), headers=dict(token=token),
                              follow_redirects=True)

        print(result.data)
        self.assertEqual(result.status_code, 200)
        user = User.nodes.get_or_none(uid=uid)

        self.assertIsNotNone(user)

    def test_get_user_by_wrong_uuid(self):
        """
        Should get 404 on user not found by id
        """
        # First creation should be ok returning created status (201)
        self.app.post('/user', data=self.arguments, follow_redirects=True)

        uid = 0
        result = self.app.post('/login', data=dict(username=self.username, password=self.password),
                               follow_redirects=True)

        data = json.loads(result.get_data(as_text=True))
        token = data['token']

        result = self.app.get('/user/{}'.format(uid), headers=dict(token=token),
                              follow_redirects=True)

        self.assertEqual(result.status_code, 404)
        user = User.nodes.get_or_none(uid=uid)
        self.assertIsNone(user)
