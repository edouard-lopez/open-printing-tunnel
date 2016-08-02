# -*- coding: utf-8 -*-
import logging

import docker
import docker.utils
import docker.errors
from django.conf import settings

from api import models
from api import services

docker_api = docker.Client(base_url='unix://var/run/docker.sock')
logger = logging.getLogger(__name__)


def pop_new_container(data, docker_client=None):
    image_name = 'coaxisopt_daemon'
    docker_api.pull(image_name)
    container = docker_api.create_container(
        image=image_name,
        hostname=data.get('hostname'),
        command='tail -f /dev/null',
        networking_config=get_network_config(data, docker_client)
    )
    docker_api.start(container=(container.get('Id')))
    return container


def get_network_config(data, docker_client):
    network = create_network(data, docker_client)
    network_name = docker_client.inspect_network(network.get('Id')).get('Name')
    network_info = dict()
    network_info[network_name] = docker_client.create_endpoint_config(ipv4_address=data.get('ip'))
    networking_config = docker_client.create_networking_config(network_info)
    return networking_config


def save_infos(data):
    container = data.get('container')
    company = services.get_company(data.get('user'))
    if not company:
        raise AttributeError('Employee need to belong to a company')
    description = data.get('description')

    container_obj = models.MastContainer.objects.create(
        container_id=container.get('Id'),
        company=company,
        description=description
    )

    return container_obj


def get_container_dict(container_data):
    return {
        'id': container_data.get('Id'),
        'name': container_data.get('Name'),
        'status': container_data.get('State').get('Status'),
        'gateway': get_container_gateway(container_data),
        'ipAddress': get_container_ipaddress(container_data),
    }


def destroy(container_id):
    containers = docker_api.containers(filters={'id': container_id})
    if containers:
        container_id = containers[0].get('Id')
        docker_api.stop(container_id)
        return docker_api.remove_container(container_id)


def create_network(data, docker_client):
    network_name = "opt_network_%s" % data.get('company_id')[:6]
    for network in docker_client.networks():
        if network.get('Name') == network_name:
            return network

    try:
        ipam_pool = docker.utils.create_ipam_pool(subnet=data.get('subnet'), gateway=data.get('gateway'))
        ipam_config = docker.utils.create_ipam_config(pool_configs=[ipam_pool])
        network = docker_client.create_network(network_name,
                                               driver="macvlan",
                                               ipam=ipam_config,
                                               options={"parent": settings.DEFAULT_INTERFACE})
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
