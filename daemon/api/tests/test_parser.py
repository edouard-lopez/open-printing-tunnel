import unittest

import parser
import shell


class ParserTestCase(unittest.TestCase):
    def test_parse_list_hosts_response(self):
        stdout = [
            '\tCoaxis                                  172.23.4.1',
            '\tAkema                                  172.18.0.2'
        ]

        parsed_response = parser.list_hosts(stdout)

        self.assertDictEqual(parsed_response[0], {'name': 'Coaxis', 'hostname': '172.23.4.1'})
        self.assertDictEqual(parsed_response[1], {'name': 'Akema', 'hostname': '172.18.0.2'})

    def test_can_distinguish_on_off_status(self):
        line = "Akema:autossh    on  pid: 11828, uptime: 00:20:05"
        status = parser.detect_status(line)
        self.assertEqual(status, 'on')

        line = "\tAkema                               off\tservice has not been started yet"
        status = parser.detect_status(line)
        self.assertEqual(status, 'off')

    def test_parse_status_is_off_response(self):
        stdout = [
            "\tAkema                               off\tservice has not been started yet"
        ]

        parsed_response = parser.status_is_off(stdout)

        self.assertDictEqual(parsed_response[0], {
            'name': 'Akema',
            'state': 'off',
            'help': 'service has not been started yet'
        })

    def test_parse_status_is_on_response(self):
        stdout = [
            "Akema:autossh    on  pid: 11828, uptime: 00:20:05",
            "Akema ssh"        "on  port: 9100"
        ]

        parsed_response = parser.status_is_on(stdout)

        self.assertDictEqual(parsed_response[0], {
            'name': 'Akema',
            'state': 'on',
            'uptime': '00:20:05',
            'pid': 11828,
        })


if __name__ == '__main__':
    unittest.main()
