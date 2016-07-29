import unittest

import shell


class ShellTestCase(unittest.TestCase):
    def test_can_execute_command(self):
        response = shell.execute(['echo', 'test'])
        self.assertEqual(response['success'], True)
        self.assertEqual(response['output'], ['test'])

    def test_can_return_results_as_array(self):
        response = shell.execute(['printf', 'a\nb'])
        self.assertEqual(len(response['output']), 2)

    def test_return_std_err(self):
        response = shell.execute(["ls", "non_existent_file"])
        self.assertEqual(response['output'], ['ls: cannot access \'non_existent_file\': No such file or directory'])

    def test_remove_ansi_escape_sequence(self):
        line = '\t\u001b[0;35mBlabla\u001b[0m                                  \u001b[0;36m172.18.0.2\u001b[0m'

        escaped_line = shell.escape_ansi(line)

        self.assertEqual(escaped_line, '\tBlabla                                  172.18.0.2')

    def test_remove_ansi_escape_sequences_from_array(self):
        data = [
            '\t\u001b[0;35mBlabla\u001b[0m                                  \u001b[0;36m172.18.0.2\u001b[0m',
            '\t\u001b[0;35mBlabla\u001b[0m                                  \u001b[0;36m172.18.0.2\u001b[0m'
        ]

        escaped_data = shell.clean_response(data)

        self.assertEqual(escaped_data, [
            '\tBlabla                                  172.18.0.2',
            '\tBlabla                                  172.18.0.2'
        ])


if __name__ == '__main__':
    unittest.main()
