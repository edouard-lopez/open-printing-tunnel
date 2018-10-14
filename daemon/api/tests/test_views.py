from pprint import pprint
from unittest import TestCase

from views import app

class TestIntegrations(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_api_root_url(self):
        response = self.app.get('/api/')

        self.assertDictEqual(response.json, {'results': None})

