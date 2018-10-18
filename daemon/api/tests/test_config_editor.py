import os
import tempfile
import unittest

from config_editor import ConfigEditor

if 'IN_DOCKER' in os.environ:
    TEMPLATE_PATH = os.path.join('/etc', 'mast', 'template')
else:
    working_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEMPLATE_PATH = os.path.join(working_dir, '..', 'template')


class ConfigEditorTestCase(unittest.TestCase):
    def test_config_is_empty_when_instanciating(self):
        config_editor = ConfigEditor()

        self.assertDictEqual({}, config_editor.config)

    def test_config_editor_load__default_to_empty_config(self):
        with tempfile.NamedTemporaryFile() as site_config:
            config_editor = ConfigEditor()
            content = config_editor.load(file_path=site_config.name)

            self.assertDictEqual(content, {})

    def test_config_editor_load_ignore_comment(self):
        with tempfile.NamedTemporaryFile(mode='w+t') as site_config:
            site_config.write('# some comment')
            site_config.seek(os.SEEK_SET)  # move back

            config_editor = ConfigEditor()
            content = config_editor.load(file_path=site_config.name)

            self.assertDictEqual(content, {})

    def test_config_editor_load_ignore_empty_line(self):
        with tempfile.NamedTemporaryFile(mode='w+t') as site_config:
            site_config.write('\n')
            site_config.seek(os.SEEK_SET)  # move back

            config_editor = ConfigEditor()
            content = config_editor.load(file_path=site_config.name)

            self.assertDictEqual(content, {})

    def test_config_editor_load_reformatter_file(self):
        with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as site_config:
            site_config.write('declare -- Compression="yes"')
            site_config.seek(os.SEEK_SET)  # move back

            config_editor = ConfigEditor()
            content = config_editor.load(file_path=site_config.name)

            self.assertDictEqual(content, {'Compression': 'yes'})

    def test_config_editor_load_detect_variable(self):
        with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as site_config:
            site_config.write('declare -i FOO=123\ndeclare -- BAR="abc"')
            site_config.seek(os.SEEK_SET)  # move back

            config_editor = ConfigEditor()
            content = config_editor.load(file_path=site_config.name)

            self.assertDictEqual(content, {'BAR': 'abc', 'FOO': 123})

    def test_config_editor_can_load_config_file(self):
        site_config = TEMPLATE_PATH

        config_editor = ConfigEditor()
        content = config_editor.load(file_path=site_config)

        self.assertIn('UploadLimit', content)

    def test_config_editor_update_is_idempotent(self):
        with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as site_config:
            site_config.write('declare -i UploadLimit="100"')
            site_config.seek(os.SEEK_SET)  # move back

            config_editor = ConfigEditor()
            config_editor.update(file_path=site_config.name)
            content = config_editor.load(file_path=site_config.name)

            self.assertDictEqual(content, {'UploadLimit': 100})

    def test_config_editor_update_write_new_value(self):
        with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as site_config:
            site_config.write('declare -i UploadLimit="100"')
            site_config.seek(os.SEEK_SET)  # move back

            config_editor = ConfigEditor()
            config_editor.update(file_path=site_config.name, data={'UploadLimit': 80})
            content = config_editor.load(file_path=site_config.name)

            self.assertDictEqual(content, {'UploadLimit': 80})

    def test_config_editor_edit_value_preserve_declaration_keyword(self):
        self.assertEqual(ConfigEditor().edit('declare -i UploadLimit="100"', 'UploadLimit', 200),
                         'declare -i UploadLimit=200')

    def test_config_editor_update_preserve_other_values(self):
        with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as site_config:
            site_config.write('declare -i UploadLimit="100"\ndeclare -i DownloadLimit="10000"')
            site_config.seek(os.SEEK_SET)  # move back

            config_editor = ConfigEditor()
            config_editor.update(file_path=site_config.name, data={'UploadLimit': 80})
            content = config_editor.load(file_path=site_config.name)

            self.assertDictEqual(content, {'UploadLimit': 80, 'DownloadLimit': 10000})

    def test_config_editor_update_play_nice_with_real_file(self):
        site_config = TEMPLATE_PATH
        content = ConfigEditor().load(file_path=site_config)
        backup_value = content.get('UploadLimit')

        ConfigEditor().update(file_path=site_config, data={'UploadLimit': 80})
        content = ConfigEditor().load(file_path=site_config)

        self.assertEqual(content.get('UploadLimit'), 80)
        self.assertEqual(content.get('DownloadLimit'), 10000)
        # restore initial value
        ConfigEditor().update(file_path=site_config, data={'UploadLimit': backup_value})

    def test_parse_bash_boolean_declaration(self):
        bash_boolean = 'declare -- BandwidthLimitation="true"'

        parsed_boolean = ConfigEditor().parse(bash_boolean)

        self.assertDictEqual(parsed_boolean, {'BandwidthLimitation': 'true'})

    def test_parse_bash_integer_declaration(self):
        bash_integer = 'declare -i UploadLimit="100"'

        parsed_integer = ConfigEditor().parse(bash_integer)

        self.assertDictEqual(parsed_integer, {'UploadLimit': 100})

    def test_parse_ruleset_declaration(self):
        ruleset = 'declare -a ForwardPort=([0]="L *:9102:10.0.1.8:9100 # pc-ed" [1]="L *:9166:8.8.8.8:9100 # google")'

        parsed_array = ConfigEditor().parse(ruleset)

        self.assertDictEqual(parsed_array, {
            'ForwardPort': '([0]="L *:9102:10.0.1.8:9100 # pc-ed" [1]="L *:9166:8.8.8.8:9100 # google")'})

    def test_parse_empty_ruleset_declaration(self):
        with self.assertRaises(Exception):
            parsed_array = ConfigEditor().parse('')

    def test_cast_integer(self):
        self.assertEqual(ConfigEditor().cast_to_int('""'), 0)
        self.assertEqual(ConfigEditor().cast_to_int('"0"'), 0)
        self.assertEqual(ConfigEditor().cast_to_int('"100"'), 100)
        self.assertEqual(ConfigEditor().cast_to_int('"2.6"'), 2)

    def test_cast_string(self):
        self.assertEqual(ConfigEditor().cast('""', "--"), '')
        self.assertEqual(ConfigEditor().cast('"yes"', "--"), 'yes')
        self.assertEqual(ConfigEditor().cast('"true"', "--"), 'true')

    def test_parse_forward_rule_can_parse_empty(self):
        ruleset = 'declare -a ForwardPort=()'

        parsed = ConfigEditor().parse_forward_ruleset(ruleset)

        self.assertListEqual(parsed, [])

    def test_parse_forward_rule_return_object(self):
        ruleset = 'declare -a ForwardPort=([0]="L *:9102:10.0.1.8:9100 # bureau étage")'

        parsed = ConfigEditor().parse_forward_ruleset(ruleset)

        self.assertListEqual(parsed, [{
            'id': -1,
            'description': 'bureau étage',
            'hostname': '10.0.1.8',
            'ports': {
                'send': 9100,
                'forward': 'remote',
                'listen': 9102
            }
        }])

    def test_serialize_forward_rule(self):
        rule = {
            'description': 'bureau étage',
            'hostname': '10.0.1.8',
            'ports': {'send': 9100, 'forward': 'remote', 'listen': 9102}
        }

        serialization = ConfigEditor().serialize_forward_rule(rule)

        self.assertEqual(serialization, '"L *:9102:10.0.1.8:9100 # bureau étage"')

    def test_serialize_forward_ruleset_empty_ruleset(self):
        ruleset = []

        serialization = ConfigEditor().serialize_forward_ruleset(ruleset)

        self.assertEqual(serialization, '()')

    def test_serialize_forward_ruleset(self):
        ruleset = [
            {
                'description': 'étage',
                'hostname': '1.2.3.4',
                'ports': {'send': 9100, 'forward': 'remote', 'listen': 9101}
            },
            {
                'description': 'rdc',
                'hostname': '8.8.8.8',
                'ports': {'send': 9100, 'forward': 'remote', 'listen': 9102}
            }
        ]

        serialization = ConfigEditor().serialize_forward_ruleset(ruleset)

        self.assertEqual(serialization, '([0]="L *:9101:1.2.3.4:9100 # étage" [1]="L *:9102:8.8.8.8:9100 # rdc")')

    def test_aggregate_site_config_no_site_yet(self):
        sites = []

        listening_ports = ConfigEditor().aggregate_listening_ports(sites)

        self.assertListEqual(listening_ports, [])

    def test_aggregate_site_config_no_printer(self):
        sites = [{'id': 'paris', 'channels': []}]

        listening_ports = ConfigEditor().aggregate_listening_ports(sites)

        self.assertListEqual(listening_ports, [])

    def test_aggregate_site_config(self):
        sites = [
            {'id': 'paris', 'channels': [
                {'ports': {'listen': 9101}},
                {'ports': {'listen': 9105}}
            ]},
            {'id': 'bayonne', 'channels': [{'ports': {'listen': 9103}}]}
        ]

        listening_ports = ConfigEditor().aggregate_listening_ports(sites)

        self.assertListEqual(listening_ports, [9101, 9103, 9105])
