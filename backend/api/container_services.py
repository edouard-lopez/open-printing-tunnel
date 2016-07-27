# -*- coding: utf-8 -*-
import logging
import uuid

import docker
import docker.utils
import docker.errors

from api import models
from api import services

docker_api = docker.Client(base_url='unix://var/run/docker.sock')
logger = logging.getLogger(__name__)


def pop_new_container(data):
    image_name = 'busybox:latest'
    docker_api.pull(image_name)
    container = docker_api.create_container(
        image=image_name,
        name='mast__{}'.format(uuid.uuid4()),
        hostname=data.get('hostname'),
        command='tail -f /dev/null'
    )
    docker_api.start(container=(container.get('Id')))
    return container


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
        'gateway': container_data.get('NetworkSettings').get('Gateway'),
        'ipAddress': container_data.get('NetworkSettings').get('IPAddress'),
        # 'verbatim': container_data
    }


def destroy(container_id):
    container = docker_api.containers(filters={'id': container_id})
    if len(container) == 1:
        docker_api.stop(container.get('Id'))
        return docker_api.remove_container(container.get('Id'))


def create_network(data, docker_client):
    network_name = "opt_network_%s" % data.get('client_id')
    for network in docker_client.networks():
        if network.get('Name') == network_name:
            return network

    try:
        ipam_pool = docker.utils.create_ipam_pool(subnet=data.get('subnet'))
        ipam_config = docker.utils.create_ipam_config(pool_configs=[ipam_pool])
        network = docker_client.create_network(network_name,
                                               driver="bridge",
                                               ipam=ipam_config,
                                               options={"com.docker.network.bridge.host_binding_ipv4": "0.0.0.0"})
        return network
    except Exception as e:
        logger.exception(e)
        raise
