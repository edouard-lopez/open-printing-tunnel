import unittest

import parser
import shell


class ParserTestCase(unittest.TestCase):
    def test_parse_list_hosts_response(self):
        stdout = [
            '3W                                     10.100.7.49',
            'Akema                              88.116.12.46'
        ]

        parsed_response = parser.list_hosts(stdout)

        self.assertDictEqual(parsed_response[0], {'name': '3W', 'hostname': '10.100.7.49'})
        self.assertDictEqual(parsed_response[1], {'name': 'Akema', 'hostname': '88.116.12.46'})

    def test_can_detect_status_state(self):
        line = "Akema:autossh                      on    pid: 19569, uptime: 30-16:22:00"
        status = parser.detect_status_state(line)
        self.assertEqual(status, 'on')

        line = "Akema                               off\tservice has not been started yet"
        status = parser.detect_status_state(line)
        self.assertEqual(status, 'off')

    def test_parse_status_is_off_response(self):
        stdout = [
            "Akema                               off\tservice has not been started yet"
        ]

        parsed_response = parser.status_is_off(stdout)

        self.assertDictEqual(parsed_response[0], {
            'name': 'Akema',
            'state': 'off',
            'help': 'service has not been started yet'
        })

    def test_parse_status_is_on_response(self):
        stdout = [
            "Akema:autossh                      on    pid: 19569, uptime: 30-16:22:00",
            "          ssh                          on    port: 22,80,81,3389"
        ]

        parsed_response = parser.status_is_on(stdout)

        self.assertDictEqual(parsed_response[0], {
            'name': 'Akema',
            'state': 'on',
            'uptime': '30-16:22:00',
            'pid': 19569,
        })

    def test_parse_start(self):
        stdout = [
            "Starting mast Akema",
            "latency                                waiting   wait a maximum of 5s before failing",
            "starting tunnel                        done  pid 26348"
        ]

        response = parser.start(stdout)

        self.assertDictEqual(response, {
            'name': 'Akema',
            'status': 'started',
            'pid': 26348,
        })

    def test_detect_start_state(self):
        stdout = [
            "Starting mast Akema",
            "latency                                waiting   wait a maximum of 5s before failing",
            "starting tunnel                        done  pid 26348"
        ]
        status = parser.detect_start_state(stdout[2])
        self.assertEqual(status, 'done')

        stdout = [
            "Starting mast Akema",
            "starting tunnel  failed\tempty pid: 11828"
        ]
        status = parser.detect_start_state(stdout[1])
        self.assertEqual(status, 'failed')

    def test_parse_start_optbox_name(self):
        line = "Starting mast Akema"

        name = parser.get_start_optbox_name(line)

        self.assertEqual(name, 'Akema')

    def test_parse_start_optbox_pid(self):
        line = "starting tunnel                        done  pid 26348"
        pid = parser.start_get_optbox_pid(line)
        self.assertEqual(pid, 26348)

        line = "starting tunnel  failed\tempty pid: 26348"
        pid = parser.start_get_optbox_pid(line)
        self.assertEqual(pid, 26348)

    def test_detect_stop_state(self):
        stdout = [
            "Stopping mast Akema",
            "stopping tunnel  skipped\talready stopped"
        ]
        status = parser.detect_stop_state(stdout[1])
        self.assertEqual(status, 'skipped')

        stdout = [
            "Stopping mast Akema",
            "stoping tunnel                         done  pid 26149"
        ]
        status = parser.detect_stop_state(stdout[1])
        self.assertEqual(status, 'done')

        stdout = [
            "Stopping mast Akema",
            "stopping tunnel  failed\tempty pid: 11828"
        ]
        status = parser.detect_stop_state(stdout[1])
        self.assertEqual(status, 'failed')

    def test_parse_stop_optbox_name(self):
        line = "Stopping mast Akema"

        name = parser.get_stop_optbox_name(line)

        self.assertEqual(name, 'Akema')

    def test_parse_stop_optbox_pid(self):
        line = "stoping tunnel                         done  pid 26149"
        pid = parser.stop_get_optbox_pid(line)
        self.assertEqual(pid, 26149)

        line = "stopping tunnel  failed\tempty pid: 26149"
        pid = parser.stop_get_optbox_pid(line)
        self.assertEqual(pid, 26149)

    def test_parse_restart(self):
        stdout = [
            "Stopping mast Akema",
            "restarting tunnel                      done  pid 26348",
            "Starting mast Akema",
            "latency                                waiting   wait a maximum of 5s before failing",
            "restarting tunnel                      done  pid 26453",
        ]

        response = parser.restart(stdout)

        self.assertDictEqual(response, {
            'name': 'Akema',
            'status': 'restarted',
            'pid': 26453,
        })



if __name__ == '__main__':
    unittest.main()
