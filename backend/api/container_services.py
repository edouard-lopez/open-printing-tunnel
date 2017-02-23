# -*- coding: utf-8 -*-
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
        networking_config=get_network_config(data, docker_client)
    )
    docker_api.start(container=container.get('Id'))
    return container


def get_network_config(data, docker_client):
    network = create_network(data, docker_client)
    network_name = docker_client.inspect_network(network.get('Id')).get('Name')
    network_info = dict()
    network_info[network_name] = docker_client.create_endpoint_config(ipv4_address=data.get('ip'))
    networking_config = docker_client.create_networking_config(network_info)
    return networking_config


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
        print(container_id)
        return docker_client.restart(container_id)