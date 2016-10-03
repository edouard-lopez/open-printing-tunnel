import unittest

from network_tools import NetworkTools


class NetworkToolsTestCase(unittest.TestCase):
    def test_can_prepare_snmp_results(self):
        infos = (
            ((1, 3, 6, 1, 2, 1, 25, 3, 2, 1, 3, 1), b'Brother HL-5250DN series'),
            ((1, 3, 6, 1, 2, 1, 1, 4, 0), b''),
            ((1, 3, 6, 1, 2, 1, 1, 1, 0), b'Brother NC-6400h, Firmware Ver.1.01  (05.08.31),MID 84UZ92'),
            ((1, 3, 6, 1, 2, 1, 1, 5, 0), b'BRN_7D3B43'),
            ((1, 3, 6, 1, 2, 1, 1, 3, 0), 168725415),
            ((1, 3, 6, 1, 2, 1, 43, 10, 2, 1, 4, 1, 1), 22629)
        )

        results = NetworkTools.format_snmp_results(infos)

        self.assertListEqual(results, [
            {'oid': '.1.3.6.1.2.1.25.3.2.1.3.1', 'value': 'Brother HL-5250DN series'},
            {'oid': '.1.3.6.1.2.1.1.4.0', 'value': ''},
            {'oid': '.1.3.6.1.2.1.1.1.0', 'value': 'Brother NC-6400h, Firmware Ver.1.01  (05.08.31),MID 84UZ92'},
            {'oid': '.1.3.6.1.2.1.1.5.0', 'value': 'BRN_7D3B43'},
            {'oid': '.1.3.6.1.2.1.1.3.0', 'value': 168725415},
            {'oid': '.1.3.6.1.2.1.43.10.2.1.4.1.1', 'value': 22629},
        ])