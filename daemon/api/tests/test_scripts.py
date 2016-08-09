import unittest

import mast_utils
import scripts


class TemplateTestCase(unittest.TestCase):
    def test_can_generate_simple_file_from_template(self):
        filename = 'printer.bat.j2'

        content = scripts.render(filename, {
            'vps': 'akema.opt',
            'imp': '1.2.3.4',
            'port': '9104',
            'site': 'akema.opt',
            'name': 'akema',
            'UTC': '2016-08-13 13:04:08'
        })

        self.assertRegex(content, 'akema.opt')
        self.assertRegex(content, '1.2.3.4')
        self.assertRegex(content, '9104')
        self.assertRegex(content, 'akema.opt')
        self.assertRegex(content, 'akema')
        self.assertRegex(content, '2016-08-13 13:04:08')

    def test_can_generate_concatenation_of_scripts(self):
        filename = 'site.bat.j2'

        content = scripts.render(filename, {'sites': [
            {'vps': 'akema.opt', 'imp': '1.2.3.4', 'port': '9101', 'name': 'akema'},
            {'vps': 'akema.opt', 'imp': '1.2.3.5', 'port': '9102', 'name': 'akema'},
            {'vps': 'akema.opt', 'imp': '1.2.3.6', 'port': '9103', 'name': 'akema'}
        ]})

        self.assertRegex(content, 'akema.opt')
        self.assertRegex(content, '1.2.3.4')
        self.assertEqual(content.count('-h akema.opt'), 3)

    def test_can_prepare_printer_install_data(self):
        printer = {
            'id': 0,
            'forward': 'normal',
            'listening_port': 9102,
            'destination_port': 9100,
            'hostname': '10.100.7.48',
            'description': 'Samsung ML3710'
        }

        site_id = 'akema'
        site_host = 'akema.coaxis.opt'
        data = scripts.prepare_printer_install_data(site_id, printer, site_host)

        self.assertDictEqual(data, {
            'port': 9102,
            'vps': 'akema.coaxis.opt',
            'imp': '10.100.7.48',
            'name': 'akema'
        })

    def test_can_prepare_site_install_data(self):
        printers = [
            {
                'id': 0,
                'forward': 'normal',
                'listening_port': 9102,
                'destination_port': 9100,
                'hostname': '10.100.7.48',
                'description': 'Samsung ML3710'
            },
            {
                'id': 1,
                'forward': 'normal',
                'listening_port': 9103,
                'destination_port': 9100,
                'hostname': '10.100.7.47',
                'description': 'Ricoh Aficio MPC300'
            },
        ]
        site_id = 'akema'
        site_host = 'akema.coaxis.opt'
        data = scripts.prepare_site_install_data(site_id, printers, site_host)

        self.assertEqual(len(data), 2)
        self.assertListEqual(data, [
            {
                'port': 9102,
                'vps': 'akema.coaxis.opt',
                'imp': '10.100.7.48',
                'name': 'akema'
            },
            {
                'port': 9103,
                'vps': 'akema.coaxis.opt',
                'imp': '10.100.7.47',
                'name': 'akema'
            },
        ])

    def test_can_return_printer_from_list(self):
        printers = [
            {
                'id': 0,
                'forward': 'normal',
                'listening_port': 9102,
                'destination_port': 9100,
                'hostname': '10.100.7.48',
                'description': 'Samsung ML3710'
            },
            {
                'id': 1,
                'forward': 'normal',
                'listening_port': 9103,
                'destination_port': 9100,
                'hostname': '10.100.7.47',
                'description': 'Ricoh Aficio MPC300'
            },
        ]
        printer = mast_utils.get_printer(printers, id=1)

        self.assertDictEqual(printer, {
            'id': 1,
            'forward': 'normal',
            'listening_port': 9103,
            'destination_port': 9100,
            'hostname': '10.100.7.47',
            'description': 'Ricoh Aficio MPC300'
        }, )
