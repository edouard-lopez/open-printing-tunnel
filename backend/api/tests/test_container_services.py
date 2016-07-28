import docker
import docker.errors

from rest_framework.test import APITestCase

from api import container_services, models
from api.tests import factories
from api.tests import mock


class ContainersTestCase(APITestCase):
    def setUp(self):
        self.docker_api = docker.Client(base_url='unix://var/run/docker.sock')
        self.company = factories.CompanyFactory(name='Akema')
        self.employee = factories.EmployeeFactory(companies=[self.company])

    def test_create_network(self):
        number_networks = len(self.docker_api.networks())
        network = container_services.create_network(data={'company_id': 'fe234e', 'subnet': '1.0.0.0/24'},
                                                    docker_client=self.docker_api)
        self.assertEqual(number_networks + 1, len(self.docker_api.networks()))
        self.docker_api.remove_network(network.get('Id'))

    def test_network_is_linked_to_the_host(self):
        network = container_services.create_network(data={'company_id': 'fe234e', 'subnet': '1.1.0.0/24'},
                                                    docker_client=self.docker_api)
        listen_on_all_interfaces = self.docker_api.inspect_network(network.get('Id')).get('Options') \
            .get('com.docker.network.bridge.host_binding_ipv4')
        self.assertEqual('0.0.0.0', listen_on_all_interfaces)
        self.docker_api.remove_network(network.get('Id'))

    def test_create_existing_network_return_old_network(self):
        number_networks = len(self.docker_api.networks())
        network = container_services.create_network(data={'company_id': 'fe234e', 'subnet': '1.2.0.0/24'},
                                                    docker_client=self.docker_api)
        network2 = container_services.create_network(data={'company_id': 'fe234e', 'subnet': '1.2.0.0/24'},
                                                     docker_client=self.docker_api)
        self.assertEqual(number_networks + 1, len(self.docker_api.networks()))
        self.assertEqual(network.get('Id'), network2.get('Id'))
        self.docker_api.remove_network(network.get('Id'))

    def test_create_network_create_bridge_base_on_shorten_company_id(self):
        network = container_services.create_network(data={'company_id': 'fe234e12dc', 'subnet': '1.3.0.0/24'},
                                                    docker_client=self.docker_api)
        bridge_name = self.docker_api.inspect_network(network.get('Id')).get('Name')
        self.assertEqual('opt_network_fe234e', bridge_name)
        self.docker_api.remove_network(network.get('Id'))

    def test_can_save_infos(self):
        container = {'Id': '9959ea03-685b-4437-ab49-c5d0a28b15e8'}

        container_services.save_infos({'user': self.employee,
                                       'container': container,
                                       'description': 'blabla'
                                       })
        containers = models.MastContainer.objects.all()

        self.assertEqual(len(containers), 1)

    def test_can_not_save_infos_when_employee_has_no_company(self):
        container = {'Id': '9959ea03-685b-4437-ab49-c5d0a28b15e8'}
        self.orphan_employee = factories.EmployeeFactory(companies=[])

        with self.assertRaises(AttributeError):
            container_services.save_infos({'user': self.orphan_employee,
                                           'container': container,
                                           'description': 'blabla'
                                           })

    def test_can_get_container_infos(self):
        container_data = mock.get_one_container_data()

        infos = container_services.get_container_dict(container_data)
        self.assertDictEqual(infos, {
            'id': 'a5775b3cf95c465d5abcee59934c087cad9ca3d20bee266c44576b7b3d06ac1c',
            'name': '/mast__e45b0231-251f-401d-b379-eb5875fc343b',
            'status': 'running',
            'gateway': '172.17.0.1',
            'ipAddress': '172.17.0.4'
        })
