import os
import unittest

import paramiko

import scanner

class ScannerTestCase(unittest.TestCase):
    def test_scan_detect_devices_on_optbox_network(self):
        hostname = '127.0.0.1/31'
        port = '9100'

        scan = scanner.scan(hostname, port)

        self.assertIsInstance(scan['scan'], dict)


    def test_scan_detect_open_port_on_optbox_network(self):
        hostname = '127.0.0.1'
        netmask = '/31'
        port = '22'

        scan = scanner.scan(hostname + netmask, port)

        self.assertIsInstance(scan['scan'], dict)

        msg = 'require ssh service to be running'
        target = scan['scan'][hostname]
        self.assertEquals(target['tcp'][22]['state'], 'open', msg)


    def test_can_get_snmp_data(self):
        printer = {
            'hostname': 'localhost',
            'port': 9100
        }

        details = scanner.get_details(printer)

        self.assertIn('contact', details)
        self.assertIn('description', details)
        self.assertEqual(details['hostname'], 'localhost')
        self.assertIn('name', details)
        self.assertIn('port', details)
        self.assertGreater(details['uptime'], 0)


    def test_open_ssh_connection(self):
        hostname = '127.0.0.1'
        username = 'coaxis'
        private_key = os.path.expanduser('~/.ssh/id_rsa.mast.coaxis')

        connection = scanner.open_ssh_connection(username, hostname, port=22, key=private_key)

        msg = 'require ssh service to be running'
        self.assertIsInstance(connection, paramiko.client.SSHClient, msg)


    def test_open_ssh_connection_raise_error(self):
        hostname = 'unreachable.host'
        username = 'coaxis'
        private_key = os.path.expanduser('~/.ssh/id_rsa.mast.coaxis')

        with self.assertRaises(Exception):
            scanner.open_ssh_connection(username, hostname, port=22, key=private_key)


    def test_fetch_netmask_from_optbox(self):
        hostname = '127.0.0.1'

        netmask = scanner.fetch_netmask(hostname)

        msg = 'require ssh service to be running'
        self.assertEqual(netmask, '/8', msg)


    def test_parse_netmask(self):
        hostname = '127.0.0.1'

        stdout = [
            "1: lo    inet 127.0.0.1/8 scope host lo\       valid_lft forever preferred_lft forever",
            "3: wlp4s0    inet 192.168.2.133/24 brd 192.168.2.255 scope global dynamic wlp4s0\       valid_lft 58984sec preferred_lft 58984sec",
            "4: docker0    inet 172.17.0.1/16 scope global docker0\       valid_lft forever preferred_lft forever",
            "5: br-a49026d1a341    inet 172.18.0.1/16 scope global br-a49026d1a341\       valid_lft forever preferred_lft forever",
            "6: br-d26f2005f732    inet 172.19.0.1/16 scope global br-d26f2005f732\       valid_lft forever preferred_lft forever",
        ]

        netmask = scanner.parse_address(hostname, stdout)

        self.assertEqual(netmask, '/8')
