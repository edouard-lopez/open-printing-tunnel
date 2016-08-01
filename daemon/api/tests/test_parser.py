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

    def test_parse_status(self):
        stdout = ["Akema                               off\tservice has not been started yet"]

        response = parser.status(stdout, 'Akema')

        self.assertIsNotNone(response[0]['name'])
        self.assertIsNotNone(response[0]['state'])

    def test_can_detect_status_state(self):
        line = "Akema:autossh                      on    pid: 19569, uptime: 30-16:22:00"
        status = parser.detect_status_state(line)
        self.assertEqual(status, 'on')

        line = "Akema                               off\tservice has not been started yet"
        status = parser.detect_status_state(line)
        self.assertEqual(status, 'off')

    def test_parse_status_is_off_response(self):
        stdout = ["Akema                               off\tservice has not been started yet"]

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

        response = parser.start(stdout, 'Akema')

        self.assertDictEqual(response, {
            'name': 'Akema',
            'status': 'started',
            'pid': 26348,
        })

    def test_parse_empty_channels_list(self):
        stdout = ["        ForwardPort array                   empty       no value in /etc/mast/Akema"]

        response = parser.start(stdout, 'Akema')

        self.assertDictEqual(response, {
            'name': 'Akema',
            'status': 'no channels',
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

    def test_parse_start_optbox_pid(self):
        line = "starting tunnel                        done  pid 26348"
        pid = parser.start_get_optbox_pid(line)
        self.assertEqual(pid, 26348)

        line = "starting tunnel  failed\tempty pid: 26348"
        pid = parser.start_get_optbox_pid(line)
        self.assertEqual(pid, 26348)

    def test_parse_stop(self):
        stdout = [
            "Stopping mast Akema",
            "stoping tunnel                         done  pid 26149"
        ]
        response = parser.stop(stdout, 'Akema')
        self.assertDictEqual(response, {
            'name': 'Akema',
            'status': 'stopped',
            'pid': 26149,
        })

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

        response = parser.restart(stdout, 'Akema')

        self.assertDictEqual(response, {
            'name': 'Akema',
            'status': 'restarted',
            'pid': 26453,
        })

    def test_detect_channel_forward_rules(self):
        host = "3W"
        forward = "L *:9102:10.100.7.48:9100         0     # Samsung ML3710"
        reverse = "R *:22:localhost:22               0     # Revers forward for use ssh git.coaxis.com at home"

        is_rule = parser.is_forward_rule(host)
        self.assertEqual(is_rule, False)
        is_rule = parser.is_forward_rule(forward)
        self.assertEqual(is_rule, True)
        is_rule = parser.is_forward_rule(reverse)
        self.assertEqual(is_rule, True)

    def test_parse_forward_rule(self):
        line1 = "L *:9102:10.100.7.48:9100         0     # Samsung ML3710"
        line2 = "L *:9103:10.100.7.47:9100         1     # Ricoh Aficio MPC300"
        line3 = "R *:22:localhost:22               0     # Revers forward for use ssh git.coaxis.com at home"

        rule1 = parser.forward_rule(line1)
        rule2 = parser.forward_rule(line2)
        rule3 = parser.forward_rule(line3)

        self.assertDictEqual(rule1, {'id': 0, 'forward': 'normal', 'port': 9102, 'hostname': '10.100.7.48',
                                     'description': 'Samsung ML3710'})
        self.assertDictEqual(rule2, {'id': 1, 'forward': 'normal', 'port': 9103, 'hostname': '10.100.7.47',
                                     'description': 'Ricoh Aficio MPC300'})
        self.assertDictEqual(rule3, {'id': 0, 'forward': 'reverse', 'port': 22, 'hostname': 'localhost',
                                     'description': 'Revers forward for use ssh git.coaxis.com at home'})

    def test_parse_list_channels(self):
        stdout = [
            "3W",
            "L *:9102:10.100.7.48:9100         0     # Samsung ML3710",
            "L *:9103:10.100.7.47:9100         1     # Ricoh Aficio MPC300",
            "Akema",
            "R *:22:localhost:22               0     # Revers forward for use ssh git.coaxis.com at home",
            "R *:80:localhost:80               1     # Revers forward for use http git.coaxis.com at home",
            "R *:3389:10.48.50.7:3389          3     # PC maison",
        ]

        response = parser.list_channels(stdout)

        self.assertEqual(len(response), 2)
        self.assertListEqual(response, [
            {
                'name': '3W',
                'channels': [
                    {'id': 0, 'forward': 'normal', 'port': 9102, 'hostname': '10.100.7.48',
                     'description': 'Samsung ML3710'},
                    {'id': 1, 'forward': 'normal', 'port': 9103, 'hostname': '10.100.7.47',
                     'description': 'Ricoh Aficio MPC300'},
                ]
            },
            {
                'name': 'Akema',
                'channels': [
                    {'id': 0, 'forward': 'reverse', 'port': 22, 'hostname': 'localhost',
                     'description': 'Revers forward for use ssh git.coaxis.com at home'},
                    {'id': 1, 'forward': 'reverse', 'port': 80, 'hostname': 'localhost',
                     'description': 'Revers forward for use http git.coaxis.com at home'},
                    {'id': 3, 'forward': 'reverse', 'port': 3389, 'hostname': '10.48.50.7', 'description': 'PC maison'},
                ]
            }
        ])


    def test_get_optbox_dict(self):
        response = [{'name': '3W'}, {'name': 'Akema'}]

        index = parser.find_optbox(response, 'Akema')

        self.assertDictEqual(response[index], {'name': 'Akema'})


if __name__ == '__main__':
    unittest.main()
