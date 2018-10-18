import unittest

from config_constraints import Constraints


class ConfigEditorTestCase(unittest.TestCase):
    def test_censor_keep_nothing_by_default(self):
        constraints = Constraints()
        config = {'Foo': None, 'Bar': None}

        censored = list(constraints.censor(config=config).keys())

        self.assertListEqual(censored, [])

    def test_censor_keep_only_given_key(self):
        constraints = Constraints()
        only = ['Allowed', 'Uncensored']
        config = {
            'Allowed': None,
            'Uncensored': None,
            'Unauthorized': 'Dangerous'
        }

        censored = list(constraints.censor(config=config, keep=only).keys())
        censored.sort()

        self.assertListEqual(censored, ['Allowed', 'Uncensored'])

    def test_censor_empty_dict_stay_empty(self):
        constraints = Constraints()
        only = ['Allowed']
        config = {}

        censored = list(constraints.censor(config=config, keep=only).keys())

        self.assertListEqual(censored, [])
