import docker
import docker.errors

from rest_framework.test import APITestCase

from api import container_services, models
from api.tests import factories
from api.tests import mock


class ContainersTestCase(APITestCase):
    def setUp(self):
        self.docker_api = docker.Client(base_url='unix://var/run/docker.sock')
        self.client = factories.ClientFactory(name='Akema')
        self.employee = factories.EmployeeFactory(clients=[self.client])

    def test_create_network(self):
        number_networks = len(self.docker_api.networks())
        network = container_services.create_network(data={'client_id': str(self.client.id),
                                                          'subnet': '10.48.0.0/16',
                                                          'gateway': '10.48.0.200'},
                                                    docker_client=self.docker_api)
        self.assertEqual(number_networks + 1, len(self.docker_api.networks()))
        self.docker_api.remove_network(network.get('Id'))

    def test_network_use_macvlan_driver(self):
        network = container_services.create_network(data={'client_id': str(self.client.id),
                                                          'subnet': '10.48.0.0/16',
                                                          'gateway': '10.48.0.200'},
                                                    docker_client=self.docker_api)
        self.assertEqual('macvlan', self.docker_api.inspect_network(network.get('Id'))['Driver'])
        self.docker_api.remove_network(network.get('Id'))

    def test_create_existing_network_return_old_network(self):
        number_networks = len(self.docker_api.networks())
        network = container_services.create_network(data={'client_id': str(self.client.id),
                                                          'subnet': '10.48.0.0/16',
                                                          'gateway': '10.48.0.200'},
                                                    docker_client=self.docker_api)
        network2 = container_services.create_network(data={'client_id': str(self.client.id),
                                                           'subnet': '10.48.0.0/16',
                                                           'gateway': '10.48.0.200'},
                                                     docker_client=self.docker_api)
        self.assertEqual(number_networks + 1, len(self.docker_api.networks()))
        self.assertEqual(network.get('Id'), network2.get('Id'))
        self.docker_api.remove_network(network.get('Id'))

    def test_create_network_create_bridge_base_on_shorten_client_id(self):
        network = container_services.create_network(data={'client_id': 'fe234e12dc',
                                                          'subnet': '10.48.0.0/16',
                                                          'gateway': '10.48.0.200'},
                                                    docker_client=self.docker_api)
        bridge_name = self.docker_api.inspect_network(network.get('Id')).get('Name')
        self.assertEqual('opt_network_fe234e', bridge_name)
        self.docker_api.remove_network(network.get('Id'))

    def test_can_get_container_network_infos(self):
        container_data = mock.get_one_container_data()

        network_data = container_services.get_container_network_infos(container_data)

        self.assertEqual(network_data.get('IPAddress'), '10.0.0.2')

    def test_can_get_container_ipaddress(self):
        container_data = mock.get_one_container_data()

        ipaddress = container_services.get_container_ipaddress(container_data)

        self.assertEqual(ipaddress, '10.0.0.2')

    def test_can_get_container_gateway(self):
        container_data = mock.get_one_container_data()

        gateway = container_services.get_container_gateway(container_data)

        self.assertEqual(gateway, '10.0.0.1')
