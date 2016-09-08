from rest_framework.test import APITestCase, APIClient

from api import models
from api import services
from api.tests import factories


class EmployeeApiTestCase(APITestCase):
    def setUp(self):
        self.client = factories.ClientFactory(name='Akema')
        self.user = factories.UserFactory()
        self.technician = factories.TechnicianFactory(user=self.user)

        self.api_client = APIClient()
        self.api_client.force_authenticate(user=self.user)

    def test_get_employee(self):
        employee = services.get_employee(self.user)

        self.assertTrue(employee.is_technician)

    def test_create_user_call_create_employee(self):
        pass
        original_nb_of_users = models.Employee.objects.count()
        user = models.MyUser.objects.create(email='email@example.org')
        self.assertEqual(original_nb_of_users + 1, models.Employee.objects.count())
        self.assertEqual(user.employee, models.Employee.objects.filter(user__email='email@example.org').first())
        user.delete()

    def test_user_is_technician(self):
        employee = factories.EmployeeFactory()
        self.assertEqual(services.is_technician(employee.user), False)
        self.assertEqual(services.is_technician(self.technician.user), True)

    def test_admin_get_all_clients(self):
        employee_client = factories.ClientFactory(name='Coaxis')
        admin = factories.EmployeeFactory(clients=[employee_client])
        admin.user.is_admin=True

        clients = services.get_clients(admin.user)

        self.assertCountEqual(list(clients), [employee_client, self.client])

    def test_employee_get_only_his_clients(self):
        employee_client = factories.ClientFactory(name='Coaxis')
        employee = factories.EmployeeFactory(clients=[employee_client])

        clients = services.get_clients(employee.user)

        self.assertListEqual(list(clients), [employee_client])

    def test_get_employee_daemons(self):
        employee_client = factories.ClientFactory(name='Coaxis')
        employee = factories.EmployeeFactory(clients=[employee_client])
        employee_daemon = factories.DaemonFactory(client=employee_client)
        not_his_daemon = factories.DaemonFactory(client=self.client)

        daemons = services.get_daemons(employee.user)

        self.assertListEqual(list(daemons), [employee_daemon])
