import unittest

import network_utils


class NetwrokUtilsTestCase(unittest.TestCase):
    def test_telnet_is_null_when_host_unreachable(self):
        hostname = 'unreachable'
        response = {}

        response[hostname] = network_utils.telnet(hostname)

        self.assertDictEqual(response, {'unreachable': {'telnet': False}})

    def test_telnet_reply_time_when_reachable(self):
        hostname = '127.0.0.1'
        response = {}

        response[hostname] = network_utils.telnet(hostname, port=22)

        self.assertGreater(response[hostname]['telnet'], 0)

    def test_telnet_with_only_a_site(self):
        site_hostname = 'localhost'
        printers = []
        response = {}

        response = network_utils.parellelize(network_utils.telnet, site_hostname, printers)

        self.assertGreater(response[site_hostname]['telnet'], 0)

    def test_telnet_with_printers(self):
        site_hostname = 'localhost'
        printers = [
            {'hostname': '127.0.0.1', 'ports': {'send': 22}},
            {'hostname': '0.0.0.0', 'ports': {'send': 22}},
        ]

        response = network_utils.parellelize(network_utils.telnet, site_hostname, printers)

        self.assertEqual(response[site_hostname]['telnet'], True)
        self.assertEqual(response[site_hostname]['127.0.0.1']['telnet'], True)

    def test_fping_with_only_a_site(self):
        site_hostname = 'localhost'
        printers = []

        response = network_utils.ping_site_and_printers(site_hostname, printers)

        self.assertGreater(response[site_hostname]['ping'], 0)

    def test_fping_site_with_printers(self):
        site_hostname = 'localhost'
        printers = [
            {'hostname': '127.0.0.1'},
            {'hostname': '127.0.1.1'},
        ]

        response = network_utils.ping_site_and_printers(site_hostname, printers)

        self.assertGreater(response[site_hostname]['ping'], 0)
        self.assertGreater(response[site_hostname]['127.0.0.1']['ping'], 0)

    def test_dict_merge(self):
        pings = {
            'akema': {
                '1.1.1.1': {'ping': None},
                '1.2.3.4': {'ping': None},
                'ping': None,
            },
            'coaxis': {
                '1.1.1.1': {'ping': None},
                '8.8.8.8': {'ping': None},
                'ping': None,
            }
        }
        telnets = {
            'akema': {
                '1.1.1.1': {'telnet': None},
                'telnet': None,
            },
            'coaxis': {
                '1.1.1.1': {'telnet': None},
                '1.2.3.4': {'telnet': None},
                '8.8.8.8': {'telnet': None},
                'telnet': None,
            }
        }

        results = pings.copy()
        network_utils.deep_merge(results, telnets)

        self.assertDictEqual(results, {
            'akema': {
                '1.1.1.1': {'ping': None, 'telnet': None},
                '1.2.3.4': {'ping': None},
                'ping': None,
                'telnet': None,
            },
            'coaxis': {
                '1.1.1.1': {'ping': None, 'telnet': None},
                '8.8.8.8': {'ping': None, 'telnet': None},
                'ping': None,
                '1.2.3.4': {'telnet': None},
                'telnet': None,
            }
        })

    def test_benchmark_parellelize(self):
        printers = [{'hostname': '192.168.2.' + str(ip), 'ports': {'send': 22}} for ip in range(50)]
        network_utils.parellelize(network_utils.telnet, '10.0.0.1', printers)

    def test_benchmark_fping(self):
        printers = ['192.168.2.' + str(ip) for ip in range(50)]
        network_utils.fping(printers)

    def test_detect_printer(self):
        hostname = '127.0.0.1'
        mask = '/31'
        port = '9100'

        scan = network_utils.scan(hostname + mask, port)

        self.assertIsInstance(scan['scan'], dict)
        self.assertEquals(scan['scan'][hostname]['tcp'][9100]['state'], 'closed')
