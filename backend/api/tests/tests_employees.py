from rest_framework.test import APITestCase, APIClient

import api.services
from api import models
from api.tests import factories


class EmployeeApiTestCase(APITestCase):
    def setUp(self):
        self.company = factories.CompanyFactory(name='Akema')
        self.user = factories.UserFactory()
        self.technician = factories.TechnicianFactory(user=self.user)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_employee(self):
        employee = api.services.get_employee(self.user)

        self.assertTrue(employee.is_technician)

    def test_create_user_call_create_employee(self):
        pass
        original_nb_of_users = models.Employee.objects.count()
        user = models.MyUser.objects.create(email='email@example.org')
        self.assertEqual(original_nb_of_users + 1, models.Employee.objects.count())
        self.assertEqual(user.employee, models.Employee.objects.filter(user__email='email@example.org').first())
        user.delete()
