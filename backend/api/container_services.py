# -*- coding: utf-8 -*-

import docker
import docker.errors
import docker.utils
import logging
import uuid
from django.conf import settings

docker_api = docker.Client(base_url='unix://var/run/docker.sock')
logger = logging.getLogger(__name__)


def pop_new_container(data, docker_client=None):
    container = docker_api.create_container(
        image=data.get('image', 'coaxisasp/coaxisopt_daemon:latest'),
        hostname=data.get('hostname'),
        ports=[80],
        host_config=docker_api.create_host_config(
            port_bindings={80: 80},
            restart_policy={"MaximumRetryCount": 0, "Name": "always"}
        ),
        networking_config=create_network_config(data, docker_client),
        labels={'type': 'coaxisopt_daemon'}
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
        },
        'IPv4Address': network_config.get('IPAddress')
    }


def destroy(container_id):
    containers = docker_api.containers(filters={'id': container_id})
    if containers:
        container_id = containers[0].get('Id')
        docker_api.stop(container_id, 0)
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
        return docker_client.restart(container_id, 1)


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


def get_upgrade_data(container_data, version):
    return {
        'image': (get_upgrade_image(get_container_image(container_data), version)),
        'hostname': get_container_hostname(container_data),
        'volumes': create_volumes_config(container_data),
        'volumes_bindings': create_volumes_config_bindings(container_data),
        'networking_config': get_container_network_config(container_data),
        'labels': {'type': 'coaxisopt_daemon'}
    }


def get_upgrade_image(image, version):
    if get_tag(image) != version:
        info = image.split(':')
        repo_tag = info[-2]
        if len(repo_tag.split('/')) == 1:
            new_repo_tag = repo_tag
        else:
            extracted_repo_tag = repo_tag.split('/')[-2:]
            if extracted_repo_tag[0] != 'coaxisasp':
                extracted_repo_tag[0] = 'coaxisasp'
            new_repo_tag = '/'.join(extracted_repo_tag)
        image = ':'.join([new_repo_tag, version])
    return image


def upgrade_daemon_container(old_container_id, version='latest'):
    old_container_data = docker_api.inspect_container(old_container_id)
    creation_data = get_upgrade_data(old_container_data, version)

    network_id = creation_data.get('networking_config').get('EndpointsConfig').copy().popitem()[0]
    docker_api.disconnect_container_from_network(old_container_id, network_id)

    new_container = docker_api.create_container(
        image=creation_data.get('image'),
        hostname=creation_data.get('hostname'),
        volumes=creation_data.get('volumes'),
        host_config=docker_api.create_host_config(
            binds=creation_data.get('volumes_bindings'),
            port_bindings={80: 80},
            restart_policy={"MaximumRetryCount": 0, "Name": "always"}
        ),
        labels=creation_data.get('labels')
    )

    docker_api.disconnect_container_from_network(new_container.get('Id'), 'bridge')
    docker_api.connect_container_to_network(new_container.get('Id'), network_id,
                                            ipv4_address=creation_data.get('networking_config').get('IPv4Address'))
    destroy(old_container_id)
    docker_api.start(container=new_container.get('Id'))

    return docker_api.containers(filters={'id': new_container.get('Id')}).pop()


def get_networks(container_id):
    return docker_api.inspect_container(container_id)['NetworkSettings']['Networks'].copy()


def get_mounts(container_id):
    return docker_api.inspect_container(container_id)['Mounts'].copy()


def available_versions(name, images):
    versions = []

    for image in images:
        repo_tags = image.get('RepoTags', [])
        if repo_tags:
            for repo_tag in repo_tags:
                if name in repo_tag:
                    version = get_tag(repo_tag)
                    versions.append(version)

    return versions


def get_tag(repo_tag):
    return repo_tag.split(':')[-1]
