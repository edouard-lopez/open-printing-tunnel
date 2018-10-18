import unittest
from datetime import datetime

import mast_utils
import scripts_generators


class ScriptsGeneratorTestCase(unittest.TestCase):
    def test_can_generate_simple_file_from_template(self):
        filename = 'printer.bat.j2'

        content = scripts_generators.render(filename, {
            'site_hostname': 'akema.opt',
            'hostname': '1.2.3.4',
            'port': '9104',
            'site': 'akema.opt',
            'description': 'akema',
            'datetime': '2016-09-07 15:07:52'
        })

        self.assertRegex(content, 'akema.opt')
        self.assertRegex(content, '1.2.3.4')
        self.assertRegex(content, '9104')
        self.assertRegex(content, 'akema.opt')
        self.assertRegex(content, 'akema')
        self.assertRegex(content, '2016-09-07 15:07:52')

    def test_can_generate_concatenation_of_scripts(self):
        filename = 'site.bat.j2'

        content = scripts_generators.render(filename, {
            'printers': [
                {'site_hostname': 'akema.opt', 'hostname': '1.2.3.4', 'port': '9101', 'site': 'akema',
                 'description': 'lorem ipsum'},
                {'site_hostname': 'akema.opt', 'hostname': '1.2.3.5', 'port': '9102', 'site': 'akema',
                 'description': 'lorem ipsum'},
                {'site_hostname': 'akema.opt', 'hostname': '1.2.3.6', 'port': '9103', 'site': 'akema',
                 'description': 'lorem ipsum'}
            ]})

        self.assertRegex(content, 'akema.opt')
        self.assertRegex(content, '1.2.3.4')
        self.assertEqual(content.count('-h akema.opt'), 3)

    def test_can_prepare_printer_install_data(self):
        printer = {
            'id': 0,
            'ports': {
                'forward': 'remote',
                'listen': 9102,
                'send': 9100,
            },
            'hostname': '10.100.7.48',
            'description': 'Samsung ML3710',
        }

        site_id = 'akema'
        site_host = 'akema.coaxis.opt'
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        data = scripts_generators.prepare_printer_install_data(site_id, printer, site_host, now)

        self.assertDictEqual(data, {
            'port': 9102,
            'site_hostname': 'akema.coaxis.opt',
            'hostname': '10.100.7.48',
            'site': 'akema',
            'description': 'Samsung ML3710',
            'datetime': now
        })

    def test_can_prepare_site_install_data(self):
        printers = [
            {
                'id': 0,
                'ports': {'forward': 'remote', 'listen': 9102, 'send': 9100},
                'hostname': '10.100.7.48',
                'description': 'Samsung ML3710',
            },
            {
                'id': 1,
                'ports': {'forward': 'remote', 'listen': 9103, 'send': 9100},
                'hostname': '10.100.7.47',
                'description': 'Ricoh Aficio MPC300',
            },
        ]
        site_id = 'akema'
        site_host = 'akema.coaxis.opt'
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        data = scripts_generators.prepare_site_install_data(site_id, printers, site_host, now)

        self.assertEqual(len(data), 2)
        self.assertListEqual(data, [
            {
                'port': 9102,
                'site_hostname': 'akema.coaxis.opt',
                'hostname': '10.100.7.48',
                'site': 'akema',
                'description': 'Samsung ML3710',
                'datetime': now
            },
            {
                'port': 9103,
                'site_hostname': 'akema.coaxis.opt',
                'hostname': '10.100.7.47',
                'site': 'akema',
                'description': 'Ricoh Aficio MPC300',
                'datetime': now
            },
        ])

    def test_can_return_printer_from_list(self):
        printers = [
            {
                'id': 0,
                'ports': {
                    'forward': 'remote',
                    'listen': 9102,
                    'send': 9100
                },
                'hostname': '10.100.7.48',
                'description': 'Samsung ML3710',
            },
            {
                'id': 1,
                'ports': {
                    'forward': 'remote',
                    'listen': 9103,
                    'send': 9100
                },
                'hostname': '10.100.7.47',
                'description': 'Ricoh Aficio MPC300',
            },
        ]
        printer = mast_utils.get_printer(printers, id=1)

        self.assertDictEqual(printer, {
            'id': 1,
            'ports': {
                'forward': 'remote',
                'listen': 9103,
                'send': 9100
            },
            'hostname': '10.100.7.47',
            'description': 'Ricoh Aficio MPC300',
        }, )
