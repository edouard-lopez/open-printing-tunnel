import unittest

from daemon.api import shell


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

# class ServiceTestCase(unittest.TestCase):
#     def test_can_add_host(self):
#         success = mast.Service.add_host(name='home', remote_host='10.1.4.3')
#
#         self.assertEqual(success, True)



if __name__ == '__main__':
    unittest.main()
