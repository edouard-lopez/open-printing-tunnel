import socket
import unittest

import mast_utils
import network_utils


class NetwrokUtilsTestCase(unittest.TestCase):
    def test_ping_unreachable(self):
        hostname = 'unreachable'

        response = network_utils.ping(hostname)

        self.assertDictEqual(response, {
            'avg': None,
            'max': None,
            'mdev': None,
            'min': None
        })

    def test_ping_(self):
        hostname = '127.0.0.1'

        response = network_utils.ping(hostname)

        self.assertGreater(response['avg'], 0)

    def test_telnet_is_null_when_host_unreachable(self):
        hostname = 'unreachable'

        response = network_utils.telnet(hostname)

        self.assertDictEqual(response, {'unreachable': None})

    def test_telnet_give_time_when_reachable(self):
        hostname = '127.0.0.1'

        response = network_utils.telnet(hostname, port=22)

        self.assertGreater(response[hostname], 0)
