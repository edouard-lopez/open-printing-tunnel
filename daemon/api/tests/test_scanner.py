import unittest
from pprint import pprint

from scanner import Scanner
from tests.stub_network_tools import NetworkToolsStub


class ScannerTestCase(unittest.TestCase):
    def test_scan_detect_devices_on_optbox_network(self):
        scanner = Scanner(network_tools=NetworkToolsStub(), hostname='127.0.0.1')
        scan = scanner.scan(port=9100)

        self.assertIsInstance(scan['devices'], dict)

    def test_scan_detect_open_port_on_optbox_network(self):
        hostname = '10.0.1.250'
        port = '9100'
        scanner = Scanner(network_tools=NetworkToolsStub(), hostname=hostname)

        scan = scanner.scan(port=port)

        self.assertEqual(scan['devices'][hostname][port]['open'], True)

    def test_can_get_device_infos_via_snmp(self):
        scanner = Scanner(network_tools=NetworkToolsStub(), hostname='10.0.1.231')
        details = scanner.get_device_infos(hostname='10.0.1.250')

        self.assertDictEqual(details, {
            'description': {'oid': '.1.3.6.1.2.1.25.3.2.1.3.1', 'value': 'Brother HL-5250DN series'},
            'pageCount': {'oid': '.1.3.6.1.2.1.43.10.2.1.4.1.1', 'value': 22625},
            'sysContact': {'oid': '.1.3.6.1.2.1.1.4.0', 'value': ''},
            'sysDescription': {'oid': '.1.3.6.1.2.1.1.1.0', 'value': 'Brother NC-6400h, Firmware Ver.1.01  (05.08.31),MID 84UZ92'},
            'sysName': {'oid': '.1.3.6.1.2.1.1.5.0', 'value': 'BRN_7D3B43'},
            'uptime': {'oid': '.1.3.6.1.2.1.1.3.0', 'value': 143431460}
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

    def test_clean_nmap_data_to_keep_only_useful(self):
        scanner = Scanner(network_tools=NetworkToolsStub(), hostname='10.0.1.231')

        nmap = scanner.network_tools.nmap('10.0.1.231/24', 9100)
        clean = scanner.clean_nmap(nmap)

        self.assertDictEqual(clean, {
            'raw': 'nmap -oX - -p 9100 -T5 --open 10.0.1.231/24',
            'devices': {
                '10.0.1.250': {'hostname': '10.0.1.250', 'port': 9100, 'open': True},
                '10.0.1.248': {'hostname': '10.0.1.248', 'port': 9100, 'open': True}
            }
        })

    def test_add_snmp_infos(self):
        scanner = Scanner(network_tools=NetworkToolsStub(), hostname='10.0.1.231')
        nmap = {'devices': {'10.0.1.250': {'hostname': '10.0.1.250', 'port': 9100, 'open': True}}}

        results = scanner.add_snmp_infos(nmap)

        self.assertDictEqual(results['devices']['10.0.1.250'], {
            'hostname': '10.0.1.250',
            'port': 9100,
            'open': True,
            'description': {'oid': '.1.3.6.1.2.1.25.3.2.1.3.1', 'value': 'Brother HL-5250DN series'},
            'pageCount': {'oid': '.1.3.6.1.2.1.43.10.2.1.4.1.1', 'value': 22625},
            'sysContact': {'oid': '.1.3.6.1.2.1.1.4.0', 'value': ''},
            'sysDescription': {'oid': '.1.3.6.1.2.1.1.1.0',
                                'value': 'Brother NC-6400h, Firmware Ver.1.01  (05.08.31),MID 84UZ92'},
            'sysName': {'oid': '.1.3.6.1.2.1.1.5.0', 'value': 'BRN_7D3B43'},
            'uptime': {'oid': '.1.3.6.1.2.1.1.3.0', 'value': 143431460}
        })
