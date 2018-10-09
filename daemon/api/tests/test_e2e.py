import os
import unittest
from pprint import pprint

import paramiko

from network_tools import NetworkTools
from scanner import Scanner
from tests.stub_network_tools import NetworkToolsStub


class EndToEndNetworkTestCase(unittest.TestCase):
    def test_open_ssh_connection(self):
        self.skipTest('Don\'t know how to test with SSH :/')
        hostname = '127.0.0.1'
        username = 'coaxis'
        key = os.path.expanduser('~/.ssh/id_rsa')

        network_tools = NetworkTools(private_key=key)
        connection = network_tools.open_ssh_connection(username, hostname, port=22)

        msg = 'require ssh service to be running'
        self.assertIsInstance(connection, paramiko.client.SSHClient, msg)

    def test_unreachable_ssh_raise_error(self):
        hostname = 'unreachable.host'
        username = 'coaxis'
        key = os.path.expanduser('~/.ssh/id_rsa.mast.coaxis')

        network_tools = NetworkTools(private_key=key)
        with self.assertRaises(Exception):
            network_tools.open_ssh_connection(username, hostname, port=22)

    def test_get_network_interfaces(self):
        self.skipTest('Don\'t know how to test with SSH :/')
        network_tools = NetworkTools(private_key=os.path.expanduser('~/.ssh/id_rsa'))
        network_interfaces = network_tools.get_network_interfaces('127.0.0.1')

        pprint(network_interfaces)
        self.assertEqual(network_interfaces, '')

    def test_can_scan(self):
        self.skipTest('Don\'t know how to test with SSH :/')
        scanner = Scanner(network_tools=NetworkToolsStub(), hostname='10.0.1.231')

        scan = scanner.scan(port=9100)

        self.assertDictEqual(scan, {})

    def test_snmp_resist_exception(self):
        oids = [
            '.1.3.6.1.2.1.25.3.2.1.3.1',  # HOST-RESOURCES-MIB::hrDeviceDescr.1
        ]
        mibs = ['DISMAN-EVENT-MIB']

        infos = NetworkTools.snmp('127.0.0.1', oids, mibs)

        self.assertCountEqual(infos, [{'oid': '.1.3.6.1.2.1.25.3.2.1.3.1', 'value': 'unknown'}])