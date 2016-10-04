import os
import unittest

import paramiko

from network_tools import NetworkTools
from scanner import Scanner
from tests.stub_network_tools import NetworkToolsStub


class EndToEndNetworkTestCase(unittest.TestCase):
    def test_open_ssh_connection(self):
        hostname = '127.0.0.1'
        username = 'coaxis'
        key = os.path.expanduser('~/.ssh/id_rsa.mast.coaxis')

        network_tools = NetworkTools(private_key=key)
        connection = network_tools.open_ssh_connection(username, hostname, port=22)

        msg = 'require ssh service to be running'
        self.assertIsInstance(connection, paramiko.client.SSHClient, msg)


    def test_open_ssh_connection_raise_error(self):
        hostname = 'unreachable.host'
        username = 'coaxis'
        key = os.path.expanduser('~/.ssh/id_rsa.mast.coaxis')

        network_tools = NetworkTools(private_key=key)
        with self.assertRaises(Exception):
            network_tools.open_ssh_connection(username, hostname, port=22)

    def test_get_network_interfaces(self):
        self.skipTest('todo')

    def test_can_scan(self):
        scanner = Scanner(network_tools=NetworkToolsStub(), hostname='10.0.1.231')

        scan = scanner.scan(port=9100)

        self.assertDictEqual(scan, {})