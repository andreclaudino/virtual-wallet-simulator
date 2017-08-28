from unittest.case import TestCase

from ..server import app


class BaseAPITestCase(TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.app.testing = True
