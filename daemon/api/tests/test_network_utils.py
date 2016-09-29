import unittest

import network_utils


class NetwrokUtilsTestCase(unittest.TestCase):
    def test_telnet_is_null_when_host_unreachable(self):
        hostname = 'unreachable'
        response = {hostname: network_utils.telnet(hostname)}

        self.assertDictEqual(response, {'unreachable': {'telnet': False}})

    def test_telnet_reply_time_when_reachable(self):
        hostname = '127.0.0.1'
        port = 22

        response = {hostname: network_utils.telnet(hostname, port=port)}

        msg = 'require port {} to be open'.format(port)
        self.assertGreater(response[hostname]['telnet'], 0, msg)

    def test_telnet_with_only_a_site(self):
        site_hostname = 'localhost'
        port = 22
        printers = []

        response = network_utils.parellelize(network_utils.telnet, site_hostname, printers, port=port)

        msg = 'require port {} to be open'.format(port)
        self.assertGreater(response[site_hostname]['telnet'], 0, msg)

    def test_telnet_with_printers(self):
        site_hostname = 'localhost'
        port = 22
        printers = [
            {'hostname': '127.0.0.1', 'ports': {'send': 22}},
            {'hostname': '0.0.0.0', 'ports': {'send': 22}},
        ]

        response = network_utils.parellelize(network_utils.telnet, site_hostname, printers, port=port)

        msg = 'require port {} to be open'.format(port)
        self.assertEqual(response[site_hostname]['telnet'], True, msg)
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

    @staticmethod
    def test_benchmark_parellelize():
        printers = [{'hostname': '192.168.2.' + str(ip), 'ports': {'send': 22}} for ip in range(50)]

        network_utils.parellelize(network_utils.telnet, '10.0.0.1', printers)

    @staticmethod
    def test_benchmark_fping():
        printers = ['192.168.2.' + str(ip) for ip in range(50)]
        network_utils.fping(printers)
