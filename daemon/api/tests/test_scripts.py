import unittest

from daemon.api import scripts


class TemplateTestCase(unittest.TestCase):
    def test_can_generate_simple_file_from_template(self):
        filename = 'printer.bat.j2'

        content = scripts.render(filename, {
            'vps': 'akema.opt',
            'imp': '1.2.3.4',
            'port': '9104',
            'site': 'akema',
            'name': 'on aime le TDD',
            'UTC': '2016-08-13 13:04:08'
        })

        self.assertRegex(content, 'akema.opt')
        self.assertRegex(content, '1.2.3.4')
        self.assertRegex(content, '9104')
        self.assertRegex(content, 'akema')
        self.assertRegex(content, 'on aime le TDD')
        self.assertRegex(content, '2016-08-13 13:04:08')

    def test_can_generate_concatenation_of_scripts(self):
        filename = 'site.bat.j2'

        content = scripts.render(filename, {'sites': [
            {'vps': 'akema.opt', 'imp': '1.2.3.4', 'port': '9101', 'name': 'ancien locaux'},
            {'vps': 'akema.opt', 'imp': '1.2.3.5', 'port': '9102', 'name': 'nouveau locaux'},
            {'vps': 'akema.opt', 'imp': '1.2.3.6', 'port': '9103', 'name': 'on aime le TDD'}
        ]})

        self.assertRegex(content, 'akema.opt')
        self.assertRegex(content, '1.2.3.4')
        self.assertEqual(content.count('-h akema.opt'), 3)
