import unittest

from api import shell


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


if __name__ == '__main__':
    unittest.main()
