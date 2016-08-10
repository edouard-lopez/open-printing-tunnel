import unittest

import parser
import shell


class ShellTestCase(unittest.TestCase):
    def test_can_execute_command(self):
        response = shell.execute(['echo', 'test'])
        self.assertEqual(response['cmd']['exit_status'], True)
        self.assertEqual(response['results'], ['test'])

    def test_can_return_results_as_array(self):
        response = shell.execute(['printf', 'a\nb'])
        self.assertEqual(len(response['results']), 2)

    def test_return_std_err(self):
        response = shell.execute(["ls", "non_existent_file"])
        self.assertEqual(response['results'], ['ls: cannot access \'non_existent_file\': No such file or directory'])

    def test_remove_ansi_escape_sequence(self):
        line = '\t\u001b[0;35mBlabla\u001b[0m                                  \u001b[0;36m172.18.0.2\u001b[0m'

        escaped_line = shell.escape_ansi(line)

        self.assertEqual(escaped_line, '\tBlabla                                  172.18.0.2')

    def test_ignore_empty_lines(self):
        stdout = [
            "",
            "\tAkema                               off\tservice has not been started yet"
        ]

        cleaned_response = shell.clean_response(stdout)

        self.assertEqual(len(cleaned_response), 1)

    def test_remove_ansi_escape_sequences_from_array(self):
        stdout = [
            '\t\u001b[0;35mCoaxis\u001b[0m                                  \u001b[0;36m172.18.0.2\u001b[0m',
            '\t\u001b[0;35mAkema\u001b[0m                                  \u001b[0;36m172.18.0.2\u001b[0m'
        ]

        escaped_data = shell.clean_response(stdout)

        self.assertEqual(escaped_data, [
            'Coaxis                                  172.18.0.2',
            'Akema                                  172.18.0.2'
        ])

    def test_ignore_empty_stdout(self):
        stdout = [""]

        escaped_data = shell.clean_response(stdout)

        self.assertListEqual(escaped_data, [])


if __name__ == '__main__':
    unittest.main()
