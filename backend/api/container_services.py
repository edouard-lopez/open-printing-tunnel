# -*- coding: utf-8 -*-
import json
import uuid

import docker
from api import services

from api import models

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
        config=container.get('Id'),
        company=company,
        description=description
    )

    return container_obj


def destroy(container_id):
    container = docker_api.containers(filters={'id': container_id})
    docker_api.stop(container)
    return docker_api.remove_container(container)