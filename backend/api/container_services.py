# -*- coding: utf-8 -*-
import uuid

import docker

from api import models
from api import services

docker_api = docker.Client(base_url='unix://var/run/docker.sock')


def pop_new_container():
    image_name = 'busybox:latest'
    docker_api.pull(image_name)
    container = docker_api.create_container(
        image=image_name,
        name='mast__{}'.format(uuid.uuid4()),
        command='tail -f /dev/null'
    )
    docker_api.start(container=(container.get('Id')))
    return container


def save_infos(data):
    container = data.get('container')
    company = services.get_company(data.get('user'))
    print('company', company)
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
        # 'verbatim': container_data
    }


def destroy(container_id):
    container = docker_api.containers(filters={'id': container_id})[0]
    docker_api.stop(container.get('Id'))
    return docker_api.remove_container(container.get('Id'))