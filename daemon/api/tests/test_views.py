import glob
import os
from pathlib import Path
from shutil import copyfile
from unittest import TestCase

import http_status
from views import app

if 'IN_DOCKER' in os.environ:
    TEMPLATE_PATH = Path('/etc', 'mast', 'template')
else:
    working_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEMPLATE_PATH = Path(working_dir, '..', 'template')
TEMPLATE_BACKUP_PATH = Path('/tmp', 'template').with_suffix('.bak')
FIRST_ALLOCATED_PORT = 9102  # why? should be 9100


class TestViewsIntegrations(TestCase):
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

        self.assertEqual(response.status_code, http_status.BAD_REQUEST)

    def test_POST_api_sites_endpoint_require_payload_fields(self):
        response = self.app.post('/api/sites/', json={})

        self.assertEqual(response.status_code, http_status.BAD_REQUEST)

    def test_POST_api_sites_endpoint_reject_invalid_hostname(self):
        response = self.app.post('/api/sites/', json={'id': 'paris', 'hostname': 'invalid hostname'})

        self.assertEqual(response.status_code, http_status.INTERNAL_SERVER_ERROR)

    def test_POST_api_sites_endpoint_require_id_and_hostname(self):
        response = self.app.post('/api/sites/', json={'id': 'paris', 'hostname': '0.0.0.0'})

        self.assertEqual(response.status_code, http_status.CREATED)

    def test_GET_api_sites_endpoint_fetch_newly_created_site(self):
        self.app.post('/api/sites/', json={'id': 'paris', 'hostname': '0.0.0.0'})

        response = self.app.get('/api/sites/')
        json = response.json

        self.assertIn('results', json)
        self.assertGreaterEqual(len(json['results']), 1)
        self.assertDictEqual(json['results'][0], {'channels': [], 'hostname': '0.0.0.0', 'id': 'paris'})

    def test_PUT_api_site_endpoint_reject_require_action_attribute(self):
        response = self.app.post('/api/sites/', json={})

        self.assertEqual(response.status_code, http_status.BAD_REQUEST)

    def test_PUT_api_site_endpoint_reject_invalid_action(self):
        response = self.app.post('/api/sites/', json={'action': 'invalid'})

        self.assertEqual(response.status_code, http_status.BAD_REQUEST)

    def test_PUT_api_site_endpoint_start_site(self):
        self.app.post('/api/sites/', json={'id': 'paris', 'hostname': '0.0.0.0'})

        response = self.app.put('/api/sites/paris/', json={'action': 'start'})

        self.assertEqual(response.status_code, http_status.OK)
        self.assertIn('status', response.json['results'])

    def test_PUT_api_site_endpoint_stop_site(self):
        self.app.post('/api/sites/', json={'id': 'paris', 'hostname': '0.0.0.0'})

        response = self.app.put('/api/sites/paris/', json={'action': 'stop'})

        self.assertEqual(response.status_code, http_status.OK)
        self.assertIn('status', response.json['results'])

    def test_PUT_api_site_endpoint_check_status_site(self):
        self.app.post('/api/sites/', json={'id': 'paris', 'hostname': '0.0.0.0'})

        response = self.app.put('/api/sites/paris/', json={'action': 'status'})

        self.assertEqual(response.status_code, http_status.OK)
        self.assertIn('state', response.json['results'])

    def test_PUT_api_site_endpoint_restart_site(self):
        self.app.post('/api/sites/', json={'id': 'paris', 'hostname': '0.0.0.0'})

        response = self.app.put('/api/sites/paris/', json={'action': 'restart'})
        self.assertEqual(response.status_code, http_status.OK)
        self.assertIn('status', response.json['results'])

    def test_DELETE_api_site_endpoint(self):
        self.app.post('/api/sites/', json={'id': 'paris', 'hostname': '0.0.0.0'})

        response = self.app.delete('/api/sites/paris/')

        self.assertEqual(response.status_code, http_status.OK)

    def test_POST_api_printers_require_payload(self):
        response = self.app.post('/api/printers/', json={})

        self.assertEqual(response.status_code, http_status.BAD_REQUEST)

    def test_POST_api_printers_require_payload_fields(self):
        response = self.app.post('/api/printers/', json={'site': 'paris'})

        self.assertEqual(response.status_code, http_status.BAD_REQUEST)

    def test_POST_api_printers_require_valid_hostname(self):
        response = self.app.post('/api/printers/',
                                 json={'site': 'paris', 'hostname': 'hōßt näme!', 'description': 'bureau'})

        self.assertEqual(response.status_code, http_status.BAD_REQUEST)

    def test_POST_api_printers_return_forward_rule(self):
        self.app.post('/api/sites/', json={'id': 'bordeaux', 'hostname': '0.0.0.0'})

        response = self.app.post('/api/printers/',
                                 json={'site': 'bordeaux', 'hostname': '0.0.0.0', 'description': 'bureau'})
        results = response.json['results']

        self.assertEqual(response.status_code, http_status.CREATED)
        self.assertIn('ports', results)
        ports = list(results['ports'].keys())
        ports.sort()
        self.assertListEqual(ports, ['forward', 'listen', 'send'])

    def test_POST_api_printers_return_create_new_rule(self):
        self.app.post('/api/sites/', json={'id': 'bordeaux', 'hostname': '0.0.0.0'})
        self.app.post('/api/printers/', json={'site': 'bordeaux', 'hostname': '0.0.0.0', 'description': 'bureau'})
        channels = self.app.get('/api/sites/').json['results'][0]['channels']

        self.assertEqual(len(channels), 1)
        self.assertEqual(channels[0]['ports']['listen'], FIRST_ALLOCATED_PORT)

    def test_POST_api_printers_assign_port_manually_reject_incomplete_printer_config(self):
        self.app.post('/api/sites/', json={'id': 'bordeaux', 'hostname': '0.0.0.0'})

        response = self.app.post('/api/printers/', json={
            'ports': {'listen': 9108},
            'site': 'bordeaux', 'hostname': '0.0.0.0', 'description': 'réception'
        })

        self.assertEqual(response.status_code, http_status.BAD_REQUEST)

    def test_POST_api_printers_assign_port_manually_reject_allocated_port(self):
        self.app.post('/api/sites/', json={'id': 'bordeaux', 'hostname': '0.0.0.0'})
        printer_config_on_same_port = {
            'ports': {'forward': 'remote', 'listen': 9108, 'send': 9100},
            'site': 'bordeaux', 'hostname': '0.0.0.0', 'description': 'réception'
        }
        self.app.post('/api/printers/', json=printer_config_on_same_port)

        response = self.app.post('/api/printers/', json=printer_config_on_same_port)

        self.assertEqual(response.status_code, http_status.CONFLICT)

    def test_POST_api_printers_assign_port_manually_reject_out_of_boundaries(self):
        self.app.post('/api/sites/', json={'id': 'bordeaux', 'hostname': '0.0.0.0'})

        response = self.app.post('/api/printers/', json={'ports': {'forward': 'xyz', 'listen': 123456, 'send': 9100}, 'site': 'xyz', 'hostname': 'xyz', 'description': 'xyz'})
        self.assertEqual(response.status_code, http_status.NOT_ACCEPTABLE)

        response = self.app.post('/api/printers/', json={'ports': {'forward': 'xyz', 'listen': 123456, 'send': 9100}, 'site': 'xyz', 'hostname': 'xyz', 'description': 'xyz'})
        self.assertEqual(response.status_code, http_status.NOT_ACCEPTABLE)

    def test_POST_api_printers_assign_port_manually_on_new_site(self):
        self.app.post('/api/sites/', json={'id': 'bordeaux', 'hostname': '0.0.0.0'})

        response = self.app.post('/api/printers/', json={
            'ports': {'forward': 'remote', 'listen': 9108, 'send': 9100},
            'site': 'bordeaux',
            'hostname': '0.0.0.0',
            'description': 'bureau'
        })
        channels = self.app.get('/api/sites/').json['results'][0]['channels']

        self.assertEqual(response.status_code, http_status.CREATED)
        self.assertDictEqual(response.json['results']['ports'], {'forward': 'remote', 'listen': 9108, 'send': 9100})
        self.assertEqual(len(channels), 1)
        self.assertEqual(channels[0]['ports']['listen'], 9108)

    def test_POST_api_printers_assign_port_manually_on_site_with_printers(self):
        self.app.post('/api/sites/', json={'id': 'bordeaux', 'hostname': '0.0.0.0'})
        self.app.post('/api/printers/', json={'site': 'bordeaux', 'hostname': '0.0.0.0', 'description': 'bureau'})

        response = self.app.post('/api/printers/', json={
            'ports': {'forward': 'remote', 'listen': 9108, 'send': 9100},
            'site': 'bordeaux',
            'hostname': '0.0.0.0',
            'description': 'réception'
        })
        channels = self.app.get('/api/sites/').json['results'][0]['channels']

        self.assertEqual(response.status_code, http_status.CREATED)
        self.assertDictEqual(response.json['results'], {
            'ports': {'forward': 'remote', 'listen': 9108, 'send': 9100},
            'site': 'bordeaux',
            'hostname': '0.0.0.0',
            'description': 'réception'
        })
        self.assertEqual(len(channels), 2)
        listening_ports = [channel['ports']['listen'] for channel in channels]
        listening_ports.sort()
        self.assertEqual(listening_ports, [FIRST_ALLOCATED_PORT, 9108])
