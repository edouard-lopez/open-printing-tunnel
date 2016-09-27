import unittest

import paramiko

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

    def test_scan_detect_devices_on_optbox_network(self):
        hostname = '127.0.0.1/31'
        port = '9100'

        scan = network_utils.scan(hostname, port)

        self.assertIsInstance(scan['scan'], dict)

    def test_scan_detect_open_port_on_optbox_network(self):
        hostname = '127.0.0.1'
        netmask = '/31'
        port = '22'

        scan = network_utils.scan(hostname+netmask, port)

        self.assertIsInstance(scan['scan'], dict)

        msg = 'require ssh service to be running'
        target = scan['scan'][hostname]
        self.assertEquals(target['tcp'][22]['state'], 'open', msg)

    def test_can_get_snmp_data(self):
        printer = {
            'hostname': 'localhost',
            'port': 9100
        }

        details = network_utils.get_details(printer)

        self.assertIn('contact', details)
        self.assertIn('description', details)
        self.assertEqual(details['hostname'], 'localhost')
        self.assertIn('name', details)
        self.assertIn('port', details)
        self.assertGreater(details['uptime'], 0)

    def test_open_ssh_connection(self):
        hostname = '127.0.0.1'

        connection = network_utils.open_ssh_connection(hostname, 22)

        msg = 'require ssh service to be running'
        self.assertIsInstance(connection, paramiko.client.SSHClient, msg)

    def test_open_ssh_connection_raise_error(self):
        hostname = 'unreachable.host'

        with self.assertRaises(Exception):
            network_utils.open_ssh_connection(hostname, 22)

    def test_fetch_netmask_from_optbox(self):
        hostname = '127.0.0.1'

        netmask = network_utils.fetch_netmask(hostname)

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

        netmask = network_utils.parse_address(hostname, stdout)

        self.assertEqual(netmask, '/8')
