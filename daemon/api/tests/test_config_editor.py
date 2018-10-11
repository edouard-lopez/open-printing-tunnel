import unittest
import os
import tempfile
import pprint

from config_editor import ConfigEditor

WORKING_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

            config_editor = ConfigEditor()
            content = config_editor.load(file_path=site_config.name)
            
            self.assertDictEqual(content, {})

    def test_config_editor_load_detect_variable(self):
        with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as site_config:
            site_config.write('FOO=123\nBAR="abc"')
            site_config.close()

            config_editor = ConfigEditor()
            content = config_editor.load(file_path=site_config.name)
            
            self.assertDictEqual(content, {'BAR': '"abc"', 'FOO': '123'})

    def test_config_editor_can_load_config_file(self):
        site_config = os.path.join(WORKING_DIR, '..', 'template')

        config_editor = ConfigEditor()
        content = config_editor.load(file_path=site_config)
        
        self.assertIn('UploadLimit', content)

    def test_config_editor_update_is_idempotent(self):
        with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as site_config:
            site_config.write('UploadLimit=100')
            site_config.close()

            config_editor = ConfigEditor()
            config_editor.update(file_path=site_config.name)
            content = config_editor.load(file_path=site_config.name)
            
            self.assertDictEqual(content, {'UploadLimit': '100'})

    def test_config_editor_update_write_new_value(self):
        with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as site_config:
            site_config.write('UploadLimit=100')
            site_config.close()

            config_editor = ConfigEditor()
            config_editor.update(file_path=site_config.name, data={'UploadLimit': 80})
            content = config_editor.load(file_path=site_config.name)
            
            self.assertDictEqual(content, {'UploadLimit': '80'})

    def test_config_editor_update_preserve_other_values(self):
        with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as site_config:
            site_config.write('UploadLimit=100\nDownloadLimit=10000')
            site_config.close()

            config_editor = ConfigEditor()
            config_editor.update(file_path=site_config.name, data={'UploadLimit': 80})
            content = config_editor.load(file_path=site_config.name)
            
            self.assertDictEqual(content, {'UploadLimit': '80', 'DownloadLimit': '10000'})

    def test_config_editor_update_play_nice_with_real_file(self):
        site_config = os.path.join(WORKING_DIR, '..', 'template')
        config_editor = ConfigEditor()
        content = config_editor.load(file_path=site_config)
        backup_value = content.get('UploadLimit')

        config_editor.update(file_path=site_config, data={'UploadLimit': 80})
        content = config_editor.load(file_path=site_config)
        
        self.assertEqual(content.get('UploadLimit'), '80')
        self.assertEqual(content.get('DownloadLimit'), '10000')
        # restore initial value
        config_editor.update(file_path=site_config, data={'UploadLimit': backup_value})
