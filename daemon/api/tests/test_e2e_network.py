import os
import unittest

import paramiko

import scanner


class EndToEndNetworkTestCase(unittest.TestCase):
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