from unittest import TestCase

from base.base_model import BaseModel
from base.connect_db import ConnectDB

"""
Test class to guide development of BaseModel
created by André Claudino <claudino@d2x.com.br>
"""

class TestBaseModel(TestCase):

    def setUp(self):
        # Connect database
        ConnectDB.connect_database()
        # Save a test object
        self.test = BaseModel()
        # test saving alread created object
        self.test.save()

    def test_base_model_node_creation(self):
        """
        Test if created object can be found in database
        """
        # find an object with same uid
        result = BaseModel.nodes.get(uid=self.test.uid)
        # Test if objects are the same
        self.assertEqual(self.test, result)

    def test_inactivation_of_object(self):
        """
        Instead of delete objects will be inactivated,
        this method tests inactivation while testing edit
        """
        self.test.active = False
        self.test.save()

        result = BaseModel.nodes.get(uid=self.test.uid)
        self.assertFalse(result.active)

    def test_base_model_node_delete(self):
        """
        Test if object is correctly deleted on database
        """
        # Save uid for posterior use
        uid = self.test.uid
        # Delete from database
        self.test.delete()
        # Search deleted in database
        result = BaseModel.nodes.get_or_none(uid=uid)
        self.assertIsNone(result)


