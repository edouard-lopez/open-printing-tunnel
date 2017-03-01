# -*- coding: utf-8 -*-
from pprint import pprint

import logging
import uuid

import docker
import docker.errors
import docker.utils
from django.conf import settings

docker_api = docker.Client(base_url='unix://var/run/docker.sock')
logger = logging.getLogger(__name__)


def pop_new_container(data, docker_client=None):
    container = docker_api.create_container(
        # todo: use config file
        image='docker.akema.fr:5000/coaxis/coaxisopt_daemon:latest',
        hostname=data.get('hostname'),
        ports=[80],
        host_config=docker_api.create_host_config(
            port_bindings={80: 80},
            restart_policy={"MaximumRetryCount": 0, "Name": "always"}
        ),
        networking_config=create_network_config(data, docker_client)
    )
    docker_api.start(container=container.get('Id'))
    return container


def create_network_config(data, docker_client):
    network = create_network(data, docker_client)
    network_name = docker_client.inspect_network(network.get('Id')).get('Name')
    network_info = dict()
    network_info[network_name] = docker_client.create_endpoint_config(ipv4_address=data.get('ip'))
    networking_config = docker_client.create_networking_config(network_info)

    return networking_config


def get_container_network_config(container_data):
    networks = container_data.get('NetworkSettings').get('Networks')

    network_id, network_config = networks.copy().popitem()

    return {
        'EndpointsConfig': {
            network_id: {
                'IPAMConfig': {
                    'IPv4Address': network_config.get('IPAddress')
                }
            }
        }
    }


def destroy(container_id):
    containers = docker_api.containers(filters={'id': container_id})
    if containers:
        container_id = containers[0].get('Id')
        docker_api.stop(container_id)
        return docker_api.remove_container(container_id)


def get_default_interface(data):
    default_interface = settings.DEFAULT_INTERFACE
    vlan = data.get('vlan')
    logger.debug(data)
    if vlan:
        return '{interface}.{vlan_id}'.format(interface=default_interface, vlan_id=data.get('vlan'))
    return default_interface


def create_network(data, docker_client):
    network_name = "opt_network_%s" % str(uuid.uuid4())[:6]

    try:
        ipam_pool = docker.utils.create_ipam_pool(subnet=data.get('subnet'), gateway=data.get('gateway'))
        ipam_config = docker.utils.create_ipam_config(pool_configs=[ipam_pool])
        network = docker_client.create_network(network_name,
                                               driver="macvlan",
                                               ipam=ipam_config,
                                               options={"parent": get_default_interface(data)})
        return network
    except Exception as e:
        logger.exception(e)
        raise


def get_container_network_infos(container_data):
    networks = container_data.get('NetworkSettings').get('Networks')
    for network in networks:
        return networks[network]


def get_container_ipaddress(container_data):
    return get_container_network_infos(container_data).get('IPAddress')


def get_container_gateway(container_data):
    return get_container_network_infos(container_data).get('Gateway')


def filter_opt_networks(networks):
    filtered_networks = []
    for network in networks:
        if network['Name'].startswith('opt_network_'):
            filtered_networks.append(network)
    return filtered_networks


def restart(container_id, docker_client):
    containers = docker_client.containers(filters={'id': container_id})
    if containers:
        container_id = containers[0].get('Id')
        return docker_client.restart(container_id)


def get_container_volumes(container_data):
    return container_data.get('Mounts')


def get_container_hostname(container_data):
    return container_data.get('Config').get('Hostname')


def get_container_image(container_data):
    return container_data.get('Config').get('Image')


def create_volumes_config(container_data):
    volumes = get_container_volumes(container_data)

    return [volume['Destination'] for volume in volumes]


def create_volumes_config_bindings(container_data):
    volumes = get_container_volumes(container_data)
    bindings = {}

    for volume in volumes:
        bindings[volume['Name']] = {
            'bind': volume['Destination'],
            'mode': 'rw'
        }

    return bindings


def get_upgrade_data(container_data):
    return {
        'image': get_container_image(container_data),
        'hostname': get_container_hostname(container_data),
        'volumes': create_volumes_config(container_data),
        'volumes_bindings': create_volumes_config_bindings(container_data),
        'networking_config': get_container_network_config(container_data)
    }


def upgrade_daemon_container(old_container_id):
    old_container_data = docker_api.inspect_container(old_container_id)
    creation_data = get_upgrade_data(old_container_data)

    new_container = docker_api.create_container(
        image=creation_data.get('image'),
        hostname=creation_data.get('hostname'),
        volumes=creation_data.get('volumes'),
        host_config=docker_api.create_host_config(
            binds=creation_data.get('volumes_bindings'),
            port_bindings={80: 80},
            restart_policy={"MaximumRetryCount": 0, "Name": "always"}
        ))

    return new_container