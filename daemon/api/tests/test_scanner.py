import unittest
from pprint import pprint

from scanner import Scanner
from tests.stub_network_tools import NetworkToolsStub


class ScannerTestCase(unittest.TestCase):
    def test_scan_detect_devices_on_optbox_network(self):
        scanner = Scanner(network_tools=NetworkToolsStub(), hostname='127.0.0.1')
        scan = scanner.scan(port=9100)

        self.assertIsInstance(scan['scan'], dict)

    def test_scan_detect_open_port_on_optbox_network(self):
        hostname = '10.0.1.250'
        port = 9100
        scanner = Scanner(network_tools=NetworkToolsStub(), hostname=hostname)

        scan = scanner.scan(port=port)
        pprint(scan)
        self.assertEquals(scan['scan'][hostname]['tcp'][port]['state'], 'open')

    def test_can_get_device_infos_via_snmp(self):
        scanner = Scanner(network_tools=NetworkToolsStub(), hostname='10.0.1.231')
        details = scanner.get_device_infos(hostname='10.0.1.250')

        self.assertDictEqual(details, {
            'description': {'oid': '.1.3.6.1.2.1.1.5.0', 'value': b'BRN_7D3B43'},
            'page_count': {'oid': '.1.3.6.1.2.1.1.3.0', 'value': 143431460},
            'sys_contact': {'oid': '.1.3.6.1.2.1.25.3.2.1.3.1', 'value': b'Brother HL-5250DN series'},
            'sys_description': {'oid': '.1.3.6.1.2.1.1.1.0',
                                'value': b'Brother NC-6400h, Firmware Ver.1.01  (05.08.31),MID 84UZ92'},
            'sys_name': {'oid': '.1.3.6.1.2.1.1.4.0', 'value': b''},
            'uptime': {'oid': '.1.3.6.1.2.1.43.10.2.1.4.1.1', 'value': 22625}
        })

    def test_get_netmask_from_optbox(self):
        scanner = Scanner(network_tools=NetworkToolsStub(), hostname='10.0.1.133')

        netmask = scanner.get_netmask()

        self.assertEqual(netmask, '/24')

    def test_parse_netmask(self):
        scanner = Scanner(network_tools=NetworkToolsStub(), hostname='127.0.0.1')

        stdout = [
            "1: lo    inet 127.0.0.1/8 scope host lo\       valid_lft forever preferred_lft forever",
            "3: wlp4s0    inet 10.0.1.133/24 brd 10.0.1.255 scope global dynamic wlp4s0\       valid_lft 58984sec preferred_lft 58984sec",
            "4: docker0    inet 172.17.0.1/16 scope global docker0\       valid_lft forever preferred_lft forever",
            "5: br-a49026d1a341    inet 172.18.0.1/16 scope global br-a49026d1a341\       valid_lft forever preferred_lft forever",
            "6: br-d26f2005f732    inet 172.19.0.1/16 scope global br-d26f2005f732\       valid_lft forever preferred_lft forever",
        ]

        netmask = scanner.parse_address(stdout)

        self.assertEqual(netmask, '/8')

    def test_parse_scan(self):
        scanner = Scanner(network_tools=NetworkToolsStub(), hostname='10.0.1.231')

        nmap = scanner.network_tools.nmap('10.0.1.231/24', 9100)
        parse = scanner.clean_nmap(nmap)

        self.assertDictEqual(parse, {
            'raw': 'nmap -oX - -p 9100 -T5 --open 10.0.1.231/24',
            'devices': {
                '10.0.1.250': {9100: {'open': True}},
                '10.0.1.248': {9100: {'open': True}}
            }
        })

    def test_add_snmp_infos(self):
        scanner = Scanner(network_tools=NetworkToolsStub(), hostname='10.0.1.231')
        nmap = {'devices': {'10.0.1.250': {9100: {'open': True}}}}

        results = scanner.add_snmp_infos(nmap)

        self.assertDictEqual(results['devices']['10.0.1.250'], {
            9100: {'open': True},
            'description': {'oid': '.1.3.6.1.2.1.1.5.0', 'value': b'BRN_7D3B43'},
            'page_count': {'oid': '.1.3.6.1.2.1.1.3.0', 'value': 143431460},
            'sys_contact': {'oid': '.1.3.6.1.2.1.25.3.2.1.3.1',
                            'value': b'Brother HL-5250DN series'},
            'sys_description': {'oid': '.1.3.6.1.2.1.1.1.0',
                                'value': b'Brother NC-6400h, Firmware Ver.1.01  (05.08.'
                                         b'31),MID 84UZ92'},
            'sys_name': {'oid': '.1.3.6.1.2.1.1.4.0', 'value': b''},
            'uptime': {'oid': '.1.3.6.1.2.1.43.10.2.1.4.1.1', 'value': 22625}
        })
