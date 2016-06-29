from rest_framework.test import APITestCase, APIClient

import api.services
from api.tests import factories


class EmployeeApiTestCase(APITestCase):
    def setUp(self):
        self.company = factories.CompanyFactory(name='Akema')
        self.user = factories.UserFactory(company=self.company)
        self.technician = factories.TechnicianFactory(user=self.user)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_employee(self):
        employee = api.services.get_employee(self.user)

        self.assertTrue(employee.is_technician)
