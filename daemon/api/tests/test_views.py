from unittest import TestCase

from views import app


class TestAPIIntegrations(TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_GET_api_root_endpoint(self):
        response = self.app.get('/api/')

        self.assertDictEqual(response.json, {'results': None})

    def test_POST_api_sites_endpoint_require_payload(self):
        response = self.app.post('/api/sites/')

        self.assertEqual(response.status_code, 400)

    def test_POST_api_sites_endpoint_require_payload_fields(self):
        response = self.app.post('/api/sites/', json={})

        self.assertEqual(response.status_code, 400)

    def test_POST_api_sites_endpoint_reject_invalid_hostname(self):
        response = self.app.post('/api/sites/', json={"id": "paris", "hostname": "invalid hostname"})

        self.assertEqual(response.status_code, 500)

    def test_POST_api_sites_endpoint_require_id_and_hostname(self):
        response = self.app.post('/api/sites/', json={"id": "paris", "hostname": "10.0.1.8"})

        self.assertEqual(response.status_code, 201)

    def test_GET_api_sites_endpoint(self):
        self.app.post('/api/sites/', json={"id": "paris", "hostname": "10.0.1.8"})

        response = self.app.get('/api/sites/')
        json = response.get_json()

        self.assertIn('results', json)
        self.assertGreaterEqual(len(json['results']), 1)
        self.assertIn('channels', json['results'][0])
        self.assertIn('cmd', json)
        self.assertGreaterEqual(len(json['cmd']), 1)
        self.assertEqual(json['cmd']['exit_status'], True)
