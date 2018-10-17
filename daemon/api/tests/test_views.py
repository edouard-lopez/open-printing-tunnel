import glob
import os
from pathlib import Path
from shutil import copyfile
from unittest import TestCase

from views import app

if 'IN_DOCKER' in os.environ:
    TEMPLATE_PATH = Path('/etc', 'mast', 'template')
else:
    working_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEMPLATE_PATH = Path(working_dir, '..', 'template')
TEMPLATE_BACKUP_PATH = Path('/tmp', 'template').with_suffix('.bak')


class TestAPIIntegrations(TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        copyfile(str(TEMPLATE_PATH), str(TEMPLATE_BACKUP_PATH))

    def tearDown(self):
        files = glob.glob(str(TEMPLATE_PATH.parent) + '/*')
        for file in files:
            os.remove(file)
        copyfile(str(TEMPLATE_BACKUP_PATH), str(TEMPLATE_PATH))

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
        response = self.app.post('/api/sites/', json={"id": "paris", "hostname": "0.0.0.0"})

        self.assertEqual(response.status_code, 201)

    def test_GET_api_sites_endpoint_fetch_newly_created_site(self):
        self.app.post('/api/sites/', json={"id": "paris", "hostname": "0.0.0.0"})

        response = self.app.get('/api/sites/')
        json = response.get_json()

        self.assertIn('results', json)
        self.assertGreaterEqual(len(json['results']), 1)
        self.assertDictEqual(json['results'][0], {'channels': [], 'hostname': '0.0.0.0', 'id': 'paris'})

    def test_PUT_api_site_endpoint_reject_require_action_attribute(self):
        response = self.app.post('/api/sites/', json={})

        self.assertEqual(response.status_code, 400)

    def test_PUT_api_site_endpoint_reject_invalid_action(self):
        response = self.app.post('/api/sites/', json={'action': 'invalid'})

        self.assertEqual(response.status_code, 400)

    def test_PUT_api_site_endpoint_start_site(self):
        self.app.post('/api/sites/', json={"id": "paris", "hostname": "0.0.0.0"})

        response = self.app.put('/api/sites/paris/', json={'action': 'start'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.get_json()['results'])

    def test_PUT_api_site_endpoint_stop_site(self):
        self.app.post('/api/sites/', json={"id": "paris", "hostname": "0.0.0.0"})

        response = self.app.put('/api/sites/paris/', json={'action': 'stop'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.get_json()['results'])

    def test_PUT_api_site_endpoint_check_status_site(self):
        self.app.post('/api/sites/', json={"id": "paris", "hostname": "0.0.0.0"})

        response = self.app.put('/api/sites/paris/', json={'action': 'status'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('state', response.get_json()['results'])

    def test_PUT_api_site_endpoint_restart_site(self):
        self.app.post('/api/sites/', json={"id": "paris", "hostname": "0.0.0.0"})

        response = self.app.put('/api/sites/paris/', json={'action': 'restart'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.get_json()['results'])

    def test_DELETE_api_site_endpoint(self):
        self.app.post('/api/sites/', json={"id": "paris", "hostname": "0.0.0.0"})

        response = self.app.delete('/api/sites/paris/')

        self.assertEqual(response.status_code, 200)
