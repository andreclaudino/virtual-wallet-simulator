from unittest import TestCase

from neomodel import db
from base.connect_db import ConnectDB

"""
Test class to guide development of ConnectDB
created by André Claudino <claudino@d2x.com.br>
"""

class TestConnectDb(TestCase):

    def test_access_config_file(self):
        """
        Test if config file is readable
        """
        credentials = ConnectDB.load_default_config()

        expected_keys = {'user', 'password', 'url', 'protocol', 'port'}
        found_keys = set(list(credentials.keys()))

        self.assertSetEqual(expected_keys, found_keys)

    def test_connecting_database(self):
        """
        Test connection to dabase writing an node in it
        then, reading back.

        After read, the object is deleted.
        """
        ConnectDB.connect_database()

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
