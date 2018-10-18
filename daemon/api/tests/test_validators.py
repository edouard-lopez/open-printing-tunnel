import unittest

import validators


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

    def test_silent_if_all_required_args_present(self):
        has_all = validators.has_all({'name': None, 'remote-host': None}, ['name', 'remote-host'])

        self.assertEqual(has_all, True)

    def test_fail_on_missing_required_arg(self):
        has_all = validators.has_all({'remote-host': None}, ['name', 'remote-host'])

        self.assertEqual(has_all, False)

    def test_ignore_extraneous_properties(self):
        has_all = validators.has_all({'name': None, 'remote-host': None}, ['name'])

        self.assertEqual(has_all, True)
