from django.test import RequestFactory
from rest_framework.request import Request
from rest_framework.test import APITestCase, APIClient

import api.services
from api.permissions import IsAdmin
from api.tests import factories


class PermissionsApiTestCase(APITestCase):
    def setUp(self):
        self.company = factories.CompanyFactory(name='Akema')
        self.user = factories.UserFactory()
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

    def test_employee_dont_have_privileges(self):
        employee = factories.EmployeeFactory(user=self.user)
        self.request.user = employee.user

        self.assertEqual(IsAdmin.has_object_permission(self, self.request, None, None), False)

    def test_technician_employee_have_privileges(self):
        technician = factories.TechnicianFactory(user=self.user)
        self.request.user = technician.user

        self.assertEqual(IsAdmin.has_object_permission(self, self.request, None, None), True)
