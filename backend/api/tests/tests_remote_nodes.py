from rest_framework.test import APITestCase, APIClient

from api import models
from api.tests import factories


class LogoutApiTestCase(APITestCase):
    def test_get_remote_nodes_401(self):
        response = self.client.get('/api/remote-nodes/')
        self.assertEqual(response.status_code, 401)


class LoggedinStaffApiTestCase(APITestCase):
    def setUp(self):
        self.company = factories.CompanyFactory(name='Akema')
        self.user = factories.UserFactory()
        self.technician = factories.TechnicianFactory(user=self.user)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_empty_remote_nodes(self):
        request = self.client.get('/api/remote-nodes/')
        self.assertEqual(len(request.data['results']), 0)

    def test_retrieve_its_own_remote_nodes(self):
        remote_node = factories.RemoteNodeFactory(company=self.technician.company)
        request = self.client.get('/api/remote-nodes/')
        self.assertEqual(len(request.data['results']), 1)
        self.assertEqual(request.data['results'][0]['name'], remote_node.name)

    def test_cannot_retrieve_other_remote_nodes(self):
        not_my_remote_node = factories.RemoteNodeFactory(company=factories.CompanyFactory(name='otherCompany'))
        request = self.client.get('/api/remote-nodes/%s/' % not_my_remote_node.id)
        self.assertEqual(request.status_code, 404)

    def test_delete_its_own_remote_nodes(self):
        remote_node = factories.RemoteNodeFactory(company=self.technician.company)
        self.assertEqual(models.RemoteNode.objects.all().count(), 1)
        request = self.client.delete('/api/remote-nodes/%s/' % remote_node.id)
        self.assertEqual(request.status_code, 204)
        self.assertEqual(models.RemoteNode.objects.all().count(), 0)

    def test_cannot_delete_other_remote_node(self):
        not_my_remote_node = factories.RemoteNodeFactory(company=factories.CompanyFactory(name='otherCompany'))
        self.assertNotEqual(not_my_remote_node.company.name, 'Akema')
        self.assertEqual(models.RemoteNode.objects.all().count(), 1)

        request = self.client.delete('/api/remote-nodes/%s/' % not_my_remote_node.id)
        self.assertEqual(request.status_code, 404)
        self.assertEqual(models.RemoteNode.objects.all().count(), 1)

    def test_update_remote_node(self):
        remote_node = factories.RemoteNodeFactory(company=self.technician.company)
        self.assertNotEqual(remote_node.name, 'akema')
        new_remote_node = {
            "name": "akema",
            "address": "1.2.3.4",
        }
        request = self.client.put('/api/remote-nodes/%s/' % remote_node.id, new_remote_node)
        self.assertEqual(request.status_code, 200, request.content.decode('utf-8'))
        remote_node_updated = models.RemoteNode.objects.get(id=remote_node.id)
        self.assertEqual(remote_node_updated.name, 'akema')
        self.assertEqual(remote_node_updated.address, '1.2.3.4')

    def test_cannot_update_other_remote_node(self):
        not_my_remote_node = factories.RemoteNodeFactory(company=factories.CompanyFactory(name='otherCompany'))
        self.assertNotEqual(not_my_remote_node.company.name, 'Akema')
        self.assertEqual(not_my_remote_node.name, 'open-space')
        new_remote_node = {
            "name": "akema",
            "address": "1.2.3.4",
        }
        request = self.client.put('/api/remote-nodes/%s/' % not_my_remote_node.id, new_remote_node)
        self.assertEqual(request.status_code, 404)
        self.assertEqual(models.RemoteNode.objects.all().count(), 1)
