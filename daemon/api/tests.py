import unittest

from daemon.api import shell
from daemon.api import validators


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
        self.assertEqual(response['output'], ["ls: cannot access 'non_existent_file': No such file or directory"])


class ValidatorsTestCase(unittest.TestCase):
    def test_accept_valid_ip(self):
        self.assertEqual(validators.is_valid_ip('10.1.4.1'), True)

    def test_refuse_incomplete_ip(self):
        self.assertEqual(validators.is_valid_ip('10.1'), False)

    def test_allow_boundary_ip(self):
        self.assertEqual(validators.is_valid_ip('0.0.0.0'), True)
        self.assertEqual(validators.is_valid_ip('255.255.255.255'), True)

    def test_allow_tld_host(self):
        self.assertEqual(validators.is_valid_host('example.opt'), True)

    def test_allow_subdomain_host(self):
        self.assertEqual(validators.is_valid_host('test.example.opt'), True)

    def test_allow_single_word_host(self):
        self.assertEqual(validators.is_valid_host('cubox'), True)

    def test_forbid_space_in_host(self):
        self.assertEqual(validators.is_valid_host('being stupid'), False)


if __name__ == '__main__':
    unittest.main()
