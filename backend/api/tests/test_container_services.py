import docker
from rest_framework.test import APITestCase

from api import container_services, models
from api.tests import factories


class ContainersTestCase(APITestCase):
    def setUp(self):
        self.docker_api = docker.Client(base_url='unix://var/run/docker.sock')
        self.company = factories.CompanyFactory(name='Akema')
        self.employee = factories.EmployeeFactory(company_set=[self.company])

    # see: test_pop_new_container()
    #  def tearDown(self):
    #     test_containers = self.docker_api.containers(filters={'name': 'mast__'})
    #     for container in test_containers:
    #         self.docker_api.stop(container['Id'])
    #         self.docker_api.remove_container(container['Id'])

    def test_can_save_infos(self):
        container = {'Id': '9959ea03-685b-4437-ab49-c5d0a28b15e8'}

        container_services.save_infos({'user': self.employee,
                                       'container': container,
                                       'description': 'blabla'
                                       })
        containers = models.MastContainer.objects.all()

        self.assertEqual(len(containers), 1)

    def test_can_destroy_container(self):
        self.skipTest()

    # is it really helpful?
    # def test_pop_new_container(self):
    #     container = container_services.pop_new_container()
    #
    #     self.assertEqual(container.get('Warning'), None)
