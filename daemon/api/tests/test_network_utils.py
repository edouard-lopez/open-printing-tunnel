import unittest

import network_utils


class NetwrokUtilsTestCase(unittest.TestCase):
    def test_ping_is_null_when_host_unreachable(self):
        hostname = 'unreachable'

        response = network_utils.ping(hostname)

        self.assertDictEqual(response, {
            'avg': None,
            'max': None,
            'mdev': None,
            'min': None
        })

    def test_ping_reply_time_when_reachable(self):
        hostname = '127.0.0.1'

        response = network_utils.ping(hostname)

        self.assertGreater(response['avg'], 0)

    def test_ping_with_only_a_site(self):
        site_hostname = 'localhost'
        printers = []
        response = {}

        response = network_utils.parellelize(network_utils.ping, site_hostname, printers)

        self.assertGreater(response[site_hostname]['avg'], 0)

    def test_ping_with_printers(self):
        site_hostname = 'localhost'
        printers = [
            {'hostname': '127.0.0.1', 'port': 22},
            {'hostname': '0.0.0.0', 'port': 22},
        ]

        response = network_utils.parellelize(network_utils.ping, site_hostname, printers)

        self.assertGreater(response[site_hostname]['avg'], 0)
        self.assertGreater(response[site_hostname]['127.0.0.1']['avg'], 0)

    def test_telnet_is_null_when_host_unreachable(self):
        hostname = 'unreachable'
        response = {}

        response[hostname] = network_utils.telnet(hostname)

        self.assertDictEqual(response, {'unreachable': {'telnet': None}})

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
            {'hostname': '127.0.0.1', 'port': 22},
            {'hostname': '0.0.0.0', 'port': 22},
        ]

        response = network_utils.parellelize(network_utils.telnet, site_hostname, printers)

        self.assertGreater(response[site_hostname]['telnet'], 0)
        self.assertGreater(response[site_hostname]['127.0.0.1']['telnet'], 0)
