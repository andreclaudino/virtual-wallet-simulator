from math import exp
from unittest import TestCase

from neomodel import db

from base.base_model import ConnectDb

class TestConnectDb(TestCase):

    def test_access_config_file(self):
        """
        Test if config file is readable
        """
        credentials = ConnectDb.load_default_config()

        expected_keys = {'user', 'password', 'url', 'protocol','port'}
        found_keys = set(list(credentials.keys()))

        self.assertSetEqual(expected_keys, found_keys)

    def test_connecting_database(self):
        ConnectDb.connect_database()

        db.cypher_query("""
        CREATE (TestNode:TEST {message: 'JUST FOR TESTING CONNECTION', val: 0})
        """)
        result = db.cypher_query("""
        MATCH (test {val: 0}) RETURN test.message
        """)

        db.cypher_query("""
        MATCH (test {val: 0}) delete test
        """)

        self.assertEqual('JUST FOR TESTING CONNECTION', (result[0][0][0]))
