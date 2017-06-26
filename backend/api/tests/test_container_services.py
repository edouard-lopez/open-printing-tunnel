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

        self.assertCountEqual(image, 'coaxisasp/coaxisopt_daemon:latest')

    def test_can_create_volume_config(self):
        container_data = mock.get_one_container_data()

        config = container_services.create_volumes_config(container_data)

        self.assertCountEqual(config, [
            "/home/mast/.ssh",
            "/etc/mast"
        ])

    def test_can_create_volume_bindings_config(self):
        container_data = mock.get_one_container_data()

        config = container_services.create_volumes_config_bindings(container_data)

        self.assertDictEqual(config, {
            "841d6a1709b365763c85fb4b7400c87f264d468eb1691a660fe81761da6e374f": {
                'bind': "/home/mast/.ssh",
                'mode': 'rw'
            },
            "002730cbb4dd9b37ad808915a60081508885d533fe003b529b8d0ab4fa46e92e": {
                'bind': "/etc/mast",
                'mode': 'rw'
            }
        })

    def test_can_get_network_config(self):
        container_data = mock.get_one_container_data()

        network_config = container_services.get_container_network_config(container_data)

        self.assertDictEqual(network_config, {
            'EndpointsConfig': {'opt_network_508be7': {'IPAMConfig': {'IPv4Address': '10.0.0.1'}}},
            'IPv4Address': '10.0.0.1'
        })

    def test_can_upgrade_image_version(self):
        self.assertEqual(
            container_services.get_upgrade_image('coaxisasp/coaxisopt_daemon:latest', 'beta'),
            'coaxisasp/coaxisopt_daemon:beta')
        self.assertEqual(container_services.get_upgrade_image('coaxisopt_backend:v1.6.1', 'latest'),
                         'coaxisopt_backend:latest')

    def test_can_get_data_to_upgrade_container(self):
        container_data = mock.get_one_container_data()

        creation_data = container_services.get_upgrade_data(container_data, version='beta')

        self.assertDictEqual(creation_data, {
            'image': 'coaxisasp/coaxisopt_daemon:beta',
            'hostname': 'test-01',
            'volumes': [
                '/home/mast/.ssh',
                '/etc/mast'
            ],
            'volumes_bindings': {
                '841d6a1709b365763c85fb4b7400c87f264d468eb1691a660fe81761da6e374f': {
                    'bind': '/home/mast/.ssh',
                    'mode': 'rw'
                },
                '002730cbb4dd9b37ad808915a60081508885d533fe003b529b8d0ab4fa46e92e': {
                    'bind': '/etc/mast',
                    'mode': 'rw'
                }
            },
            'networking_config': {
                'EndpointsConfig': {'opt_network_508be7': {'IPAMConfig': {'IPv4Address': '10.0.0.1'}}},
                'IPv4Address': '10.0.0.1'
            },
            'labels': {'type': 'coaxisopt_daemon'}
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

    def purge(self, containers=[]):
        for container in containers:
            self.docker_api.stop(container['Id'], 0)
            for network in self.docker_api.inspect_container(container['Id'])['NetworkSettings']['Networks']:
                if 'opt_network' in network:
                    self.docker_api.remove_network(network)
                self.docker_api.remove_container(container['Id'])

    def test_upgrade_container_pop_new_container(self):
        config = {'ip': '10.49.0.2', 'subnet': '10.49.0.0/16', 'gateway': '10.49.0.202', 'vlan': 102}
        container = container_services.pop_new_container(config, self.docker_api)

        new_container = container_services.upgrade_daemon_container(container.get('Id'))

        self.assertNotEqual(container.get('Id'), new_container.get('Id'))
        self.purge([new_container])

    def test_upgrade_container_mount_volumes_from_old_to_new_container(self):
        config = {'ip': '10.49.0.2', 'subnet': '10.49.0.0/16', 'gateway': '10.49.0.202', 'vlan': 102}
        container = container_services.pop_new_container(config, self.docker_api)

        old_container_volumes = [volume['Name'] for volume in container_services.get_mounts(container['Id'])]
        new_container = container_services.upgrade_daemon_container(container.get('Id'))
        new_container_volumes = [volume['Name'] for volume in container_services.get_mounts(new_container['Id'])]

        self.assertSetEqual(set(old_container_volumes), set(new_container_volumes))
        self.purge([new_container])

    def test_upgrade_container_bind_to_old_network(self):
        config = {'ip': '10.49.0.2', 'subnet': '10.49.0.0/16', 'gateway': '10.49.0.202', 'vlan': 102}
        container = container_services.pop_new_container(config, self.docker_api)

        old_name, old_network = container_services.get_networks(container['Id']).popitem()
        new_container = container_services.upgrade_daemon_container(container.get('Id'))
        new_name, new_network = container_services.get_networks(new_container['Id']).popitem()

        self.assertEqual(old_name, new_name)
        self.assertEqual(old_network['IPAMConfig'], new_network['IPAMConfig'])
        self.assertEqual(old_network['IPAddress'], new_network['IPAddress'])
        self.assertEqual(old_network['Gateway'], new_network['Gateway'])
        self.assertEqual(old_network['MacAddress'], new_network['MacAddress'])
        self.assertEqual(old_network['NetworkID'], new_network['NetworkID'])

        self.purge([new_container])

    def test_can_upgrade_to_different_version(self):
        config = {'ip': '10.49.0.2', 'subnet': '10.49.0.0/16', 'gateway': '10.49.0.202', 'vlan': 102,
                  'image': 'coaxisasp/coaxisopt_daemon:latest'}
        container = container_services.pop_new_container(config, self.docker_api)
        containers_count = len(self.docker_api.containers())
        beta = 'beta'
        self.docker_api.tag('coaxisopt_daemon', 'coaxisasp/coaxisopt_daemon', tag=beta)

        new_container = container_services.upgrade_daemon_container(container.get('Id'), version=beta)

        self.assertEqual(container_services.get_tag(new_container.get('Image')), 'beta')
        self.purge([new_container])

    def test_can_pop_new_container(self):
        config = {'ip': '10.49.0.2', 'subnet': '10.49.0.0/16', 'gateway': '10.49.0.202', 'vlan': 102}

        container = container_services.pop_new_container(config, self.docker_api)

        self.assertIsNotNone(container['Id'])
        self.purge([container])

    def test_can_pop_new_container_with_specific_image(self):
        config = {'ip': '10.49.0.2', 'subnet': '10.49.0.0/16', 'gateway': '10.49.0.202', 'vlan': 102,
                  'image': 'coaxisasp/coaxisopt_daemon:latest'}

        container = container_services.pop_new_container(config, self.docker_api)

        self.assertIsNotNone(container['Id'])
        self.purge([container])

    def test_can_restart_container(self):
        config = {'ip': '10.49.0.3', 'subnet': '10.49.0.0/16', 'gateway': '10.49.0.203', 'vlan': 103}
        container = container_services.pop_new_container(config, self.docker_api)
        data = self.docker_api.inspect_container(container['Id'])

        container_services.restart(container['Id'], self.docker_api)
        new_data = self.docker_api.inspect_container(container['Id'])

        self.assertGreater(new_data.get('State').get('StartedAt'), data.get('State').get('StartedAt'))
        self.purge([container])

    def test_list_available_daemons_version(self):
        images = mock.get_images()

        versions = container_services.available_versions('coaxis/coaxisopt_daemon', images)

        self.assertEqual(len(versions), 3)
        self.assertCountEqual(set(versions), {'latest', 'v1.6.1', 'v1.6.0'})

    def test_list_available_daemons_version_with_empty_repoTags(self):
        images = [
            {'RepoTags': []},
            {'RepoTags': ['node:argon-slim']},
            {'RepoTags': ['coaxisasp/coaxisopt_daemon:v1.6.0']},
            {"RepoTags": None}
        ]

        versions = container_services.available_versions('coaxis/coaxisopt_daemon', images)

        self.assertEqual(len(versions), 1)
        self.assertCountEqual(set(versions), {'v1.6.0'})

    def test_can_get_tag(self):
        repo_tag = 'coaxisasp/coaxisopt_daemon:latest'

        tag = container_services.get_tag(repo_tag)

        self.assertEqual(tag, 'latest')
