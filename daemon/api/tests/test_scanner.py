import unittest

import scanner
from scanner import Scanner
from tests.stub_network_tools import NetworkToolsStub


class ScannerTestCase(unittest.TestCase):
    def test_scan_detect_devices_on_optbox_network(self):
        scanner = Scanner(network_tools=NetworkToolsStub(), hostname='127.0.0.1')
        scan = scanner.scan(ports=9100, netmask='/31')

        self.assertIsInstance(scan['scan'], dict)

    def test_scan_detect_open_port_on_optbox_network(self):
        hostname = '192.168.2.250'
        port = 9100
        scanner = Scanner(network_tools=NetworkToolsStub(), hostname=hostname)

        scan = scanner.scan(ports=port, netmask='/31')

        self.assertEquals(scan['scan'][hostname]['tcp'][port]['state'], 'open')

    def test_can_get_details_via_snmp(self):
        scanner = Scanner(network_tools=NetworkToolsStub(), hostname='192.168.2.250')
        details = scanner.get_details()

        self.assertDictEqual(details, {
            'description': {'oid': '.1.3.6.1.2.1.1.5.0', 'value': b'BRN_7D3B43'},
            'page_count': {'oid': '.1.3.6.1.2.1.1.3.0', 'value': 143431460},
            'sys_contact': {'oid': '.1.3.6.1.2.1.25.3.2.1.3.1', 'value': b'Brother HL-5250DN series'},
            'sys_description': {'oid': '.1.3.6.1.2.1.1.1.0', 'value': b'Brother NC-6400h, Firmware Ver.1.01  (05.08.31),MID 84UZ92'},
            'sys_name': {'oid': '.1.3.6.1.2.1.1.4.0', 'value': b''},
            'uptime': {'oid': '.1.3.6.1.2.1.43.10.2.1.4.1.1', 'value': 22625}
        })


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
