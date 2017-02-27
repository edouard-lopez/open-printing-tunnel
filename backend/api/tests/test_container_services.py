import uuid

import docker
import docker.errors
from django.conf import settings
from rest_framework.test import APITestCase

from api import container_services
from api.tests import factories
from api.tests import mock


class ContainersTestCase(APITestCase):
    def setUp(self):
        self.docker_api = docker.Client(base_url='unix://var/run/docker.sock')
        self.client = factories.ClientFactory(name='Akema')
        self.client.uuid = uuid.uuid4()
        self.employee = factories.EmployeeFactory(clients=[self.client])

    def test_create_network(self):
        number_networks = len(self.docker_api.networks())
        network = container_services.create_network(data={'uuid': str(self.client.uuid),
                                                          'subnet': '10.48.0.0/16',
                                                          'gateway': '10.48.0.200'},
                                                    docker_client=self.docker_api)
        self.assertEqual(number_networks + 1, len(self.docker_api.networks()))
        self.docker_api.remove_network(network.get('Id'))

    def test_filter_network_return_only_opt_network(self):
        networks = [{"Name": "host", }, {"Name": "none", }, {"Name": "bridge", }, {"Name": "opt_default", },
                    {"Name": "opt_network_azertyuiop", }]
        filtered_networks = container_services.filter_opt_networks(networks)
        self.assertListEqual([{"Name": "opt_network_azertyuiop"}], filtered_networks)

    def test_network_use_macvlan_driver(self):
        network = container_services.create_network(data={'uuid': str(self.client.uuid),
                                                          'subnet': '10.48.0.0/16',
                                                          'gateway': '10.48.0.200'},
                                                    docker_client=self.docker_api)
        self.assertEqual('macvlan', self.docker_api.inspect_network(network.get('Id'))['Driver'])
        self.docker_api.remove_network(network.get('Id'))

    def test_network_use_custom_parent_interface_if_vlan_id(self):
        network = container_services.create_network(data={'uuid': str(self.client.uuid),
                                                          'subnet': '10.48.0.0/16',
                                                          'vlan': 100,
                                                          'gateway': '10.48.0.200'},
                                                    docker_client=self.docker_api)
        self.assertEqual('%s.100' % settings.DEFAULT_INTERFACE,
                         self.docker_api.inspect_network(network.get('Id'))['Options']['parent'])
        self.docker_api.remove_network(network.get('Id'))

    def test_network_use_custom_parent_interface_if_not_vlan_id(self):
        network = container_services.create_network(data={'uuid': str(self.client.uuid),
                                                          'subnet': '10.48.0.0/16',
                                                          'vlan': 0,
                                                          'gateway': '10.48.0.200'},
                                                    docker_client=self.docker_api)
        self.assertEqual(settings.DEFAULT_INTERFACE,
                         self.docker_api.inspect_network(network.get('Id'))['Options']['parent'])
        self.docker_api.remove_network(network.get('Id'))

    def test_can_get_container_network_infos(self):
        container_data = mock.get_one_container_data()

        network_data = container_services.get_container_network_infos(container_data)

        self.assertEqual(network_data.get('IPAddress'), '10.0.0.1')

    def test_can_get_container_ipaddress(self):
        container_data = mock.get_one_container_data()

        ipaddress = container_services.get_container_ipaddress(container_data)

        self.assertEqual(ipaddress, '10.0.0.1')

    def test_can_get_container_gateway(self):
        container_data = mock.get_one_container_data()

        gateway = container_services.get_container_gateway(container_data)

        self.assertEqual(gateway, '10.0.0.254')

    def test_can_get_container_volumes(self):
        container_data = mock.get_one_container_data()

        volumes = container_services.get_container_volumes(container_data)

        self.assertCountEqual(volumes, [
            {
                "Type": "volume",
                "Name": "841d6a1709b365763c85fb4b7400c87f264d468eb1691a660fe81761da6e374f",
                "Source": "/var/lib/docker/volumes/841d6a1709b365763c85fb4b7400c87f264d468eb1691a660fe81761da6e374f/_data",
                "Destination": "/home/mast/.ssh",
                "Driver": "local",
                "Mode": "",
                "RW": True,
                "Propagation": ""
            },
            {
                "Type": "volume",
                "Name": "002730cbb4dd9b37ad808915a60081508885d533fe003b529b8d0ab4fa46e92e",
                "Source": "/var/lib/docker/volumes/002730cbb4dd9b37ad808915a60081508885d533fe003b529b8d0ab4fa46e92e/_data",
                "Destination": "/etc/mast",
                "Driver": "local",
                "Mode": "",
                "RW": True,
                "Propagation": ""
            }
        ])

    def test_can_get_container_hostname(self):
        container_data = mock.get_one_container_data()

        hostname = container_services.get_container_hostname(container_data)

        self.assertCountEqual(hostname, 'test-01')

    def test_can_get_container_image(self):
        container_data = mock.get_one_container_data()

        image = container_services.get_container_image(container_data)

        self.assertCountEqual(image, 'docker.akema.fr:5000/coaxis/coaxisopt_daemon:latest')

    def test_can_create_volume_config(self):
        container_data = mock.get_one_container_data()

        config = container_services.create_volumes_config(container_data)

        self.assertCountEqual(config, [
            "/var/lib/docker/volumes/841d6a1709b365763c85fb4b7400c87f264d468eb1691a660fe81761da6e374f/_data",
            "/var/lib/docker/volumes/002730cbb4dd9b37ad808915a60081508885d533fe003b529b8d0ab4fa46e92e/_data"
        ])

    def test_can_create_volume_bindings_config(self):
        container_data = mock.get_one_container_data()

        config = container_services.create_volumes_config_bindings(container_data)

        self.assertDictEqual(config, {
            "/var/lib/docker/volumes/841d6a1709b365763c85fb4b7400c87f264d468eb1691a660fe81761da6e374f/_data": {
                'bind': "/home/mast/.ssh",
                'mode': 'rw'
            },
            "/var/lib/docker/volumes/002730cbb4dd9b37ad808915a60081508885d533fe003b529b8d0ab4fa46e92e/_data": {
                'bind': "/etc/mast",
                'mode': 'rw'
            }
        })

    def test_can_get_network_config(self):
        container_data = mock.get_one_container_data()

        network_config = container_services.get_container_network_config(container_data)

        self.assertDictEqual(network_config, {
            'EndpointsConfig': {'opt_network_508be7': {'IPAMConfig': {'IPv4Address': '10.0.0.1'}}}
        })

    def test_can_get_data_to_upgrade_container(self):
        container_data = mock.get_one_container_data()

        creation_data = container_services.get_upgrade_data(container_data)

        self.assertDictEqual(creation_data, {
            'image': 'docker.akema.fr:5000/coaxis/coaxisopt_daemon:latest',
            'hostname': "test-01",
            'volumes': [
                "/var/lib/docker/volumes/841d6a1709b365763c85fb4b7400c87f264d468eb1691a660fe81761da6e374f/_data",
                "/var/lib/docker/volumes/002730cbb4dd9b37ad808915a60081508885d533fe003b529b8d0ab4fa46e92e/_data"
            ],
            'volumes_bindings': {
                "/var/lib/docker/volumes/841d6a1709b365763c85fb4b7400c87f264d468eb1691a660fe81761da6e374f/_data": {
                    'bind': "/home/mast/.ssh",
                    'mode': 'rw'
                },
                "/var/lib/docker/volumes/002730cbb4dd9b37ad808915a60081508885d533fe003b529b8d0ab4fa46e92e/_data": {
                    'bind': "/etc/mast",
                    'mode': 'rw'
                }
            },
            'networking_config': {
                'EndpointsConfig': {'opt_network_508be7': {'IPAMConfig': {'IPv4Address': '10.0.0.1'}}}
            }
        })

    def test_create_network_config(self):
        number_networks = len(self.docker_api.networks())
        network_config = container_services.create_network_config(
            data={
                'ip': '10.49.0.1',
                'subnet': '10.49.0.0/16',
                'gateway': '10.49.0.201',
                'vlan': 101
            },
            docker_client=self.docker_api
        )
        network_id = list(network_config.get('EndpointsConfig').keys())[0]

        self.assertEqual(number_networks + 1, len(self.docker_api.networks()))
        self.docker_api.remove_network(network_id)

    def test_can_pop_new_container(self):
        config = {
            'ip': '10.49.0.2',
            'subnet': '10.49.0.0/16',
            'gateway': '10.49.0.202',
            'vlan': 102,
        }

        print('Starting container, wait…')
        container = container_services.pop_new_container(config, self.docker_api)
        containerId = container.get('Id')

        self.assertIsNotNone(containerId)

        networks = self.docker_api.inspect_container(containerId).get('NetworkSettings').get('Networks')
        network_id = networks.get(list(networks)[0]).get('NetworkID')
        container_services.destroy(containerId)
        self.docker_api.remove_network(network_id)

    def test_can_restart_container(self):
        config = {'ip': '10.49.0.3', 'subnet': '10.49.0.0/16', 'gateway': '10.49.0.203', 'vlan': 103,}
        print('Starting container, wait…')
        container = container_services.pop_new_container(config, self.docker_api)
        containerId = container.get('Id')
        data = self.docker_api.inspect_container(containerId)

        print('Restarting container, wait…')
        container_services.restart(containerId, self.docker_api)
        new_data = self.docker_api.inspect_container(containerId)

        self.assertGreater(new_data.get('State').get('StartedAt'), data.get('State').get('StartedAt'))

        networks = self.docker_api.inspect_container(containerId).get('NetworkSettings').get('Networks')
        network_id = networks.get(list(networks)[0]).get('NetworkID')
        container_services.destroy(containerId)
        self.docker_api.remove_network(network_id)
