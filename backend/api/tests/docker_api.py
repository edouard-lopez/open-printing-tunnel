import os
import unittest
import uuid

import docker

docker_api = docker.Client(base_url='unix://var/run/docker.sock')

def create_container():
    image_name = 'coaxisopt_daemon'
    container = docker_api.create_container(
        image=image_name,
        name='mast__{}'.format(uuid.uuid4()),
        # hostname=data.get('hostname'),
        command='tail -f /dev/null'
    )
    docker_api.start(container=(container.get('Id')))


class MyTestCase(unittest.TestCase):
    def test_something(self):
        # {'hostname': 'test.opt'}
        create_container()

if __name__ == '__main__':
    unittest.main()
