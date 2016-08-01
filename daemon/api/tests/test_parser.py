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

    def test_can_detect_status_state(self):
        line = "Akema:autossh    on  pid: 11828, uptime: 00:20:05"
        status = parser.detect_status_state(line)
        self.assertEqual(status, 'on')

        line = "\tAkema                               off\tservice has not been started yet"
        status = parser.detect_status_state(line)
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

    def test_detect_start_state(self):
        stdout = [
            "Starting mast Akema",
            "\tstarting tunnel  'done'\tpid: 11828"
        ]
        status = parser.detect_start_state(stdout[1])
        self.assertEqual(status, 'done')

        stdout = [
            "Starting mast Akema",
            "\tstarting tunnel  failed\tempty pid: 11828"
        ]
        status = parser.detect_start_state(stdout[1])
        self.assertEqual(status, 'failed')

    def test_parse_start_optbox_name(self):
        line = "Starting mast Akema"

        name = parser.get_start_optbox_name(line)

        self.assertEqual(name, 'Akema')

    def test_parse_start_optbox_pid(self):
        line = "\tstarting tunnel  'done'\tpid: 11828"
        pid = parser.start_get_optbox_pid(line)
        self.assertEqual(pid, 11828)

        line = "\tstarting tunnel  failed\tempty pid: 9821"
        pid = parser.start_get_optbox_pid(line)
        self.assertEqual(pid, 9821)

    def test_detect_stop_state(self):
        stdout = [
            "Stopping mast Akema",
            "\tstopping tunnel  skipped\talready stopped"
        ]
        status = parser.detect_stop_state(stdout[1])
        self.assertEqual(status, 'skipped')

        stdout = [
            "Stopping mast Akema",
            "\tstopping tunnel  'done'\tpid: 11828"
        ]
        status = parser.detect_stop_state(stdout[1])
        self.assertEqual(status, 'done')

        stdout = [
            "Stopping mast Akema",
            "\tstopping tunnel  failed\tempty pid: 11828"
        ]
        status = parser.detect_stop_state(stdout[1])
        self.assertEqual(status, 'failed')

    def test_parse_stop_optbox_name(self):
        line = "Stopping mast Akema"

        name = parser.get_stop_optbox_name(line)

        self.assertEqual(name, 'Akema')

    def test_parse_stop_optbox_pid(self):
        line = "\tstopping tunnel  'done'\tpid: 11828"
        pid = parser.stop_get_optbox_pid(line)
        self.assertEqual(pid, 11828)

        line = "\tstopping tunnel  failed\tempty pid: 9821"
        pid = parser.stop_get_optbox_pid(line)
        self.assertEqual(pid, 9821)

    def test_parse_restart(self):
        self.fail('not implemented')


if __name__ == '__main__':
    unittest.main()
