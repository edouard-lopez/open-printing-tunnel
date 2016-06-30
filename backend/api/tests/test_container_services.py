import docker
from rest_framework.test import APITestCase

from api import container_services, models
from api.tests import factories


class ContainersTestCase(APITestCase):
    def setUp(self):
        self.docker_api = docker.Client(base_url='unix://var/run/docker.sock')
        self.company = factories.CompanyFactory(name='Akema')
        self.employee = factories.EmployeeFactory(companies=[self.company])

    # see: test_pop_new_container()
    #  def tearDown(self):
    #     test_containers = self.docker_api.containers(filters={'name': 'mast__'})
    #     for container in test_containers:
    #         self.docker_api.stop(container['Id'])
    #         self.docker_api.remove_container(container['Id'])

    def test_can_save_infos(self):
        container = {'Id': '9959ea03-685b-4437-ab49-c5d0a28b15e8'}

        container_services.save_infos({'user': self.employee,
                                       'container': container,
                                       'description': 'blabla'
                                       })
        containers = models.MastContainer.objects.all()

        self.assertEqual(len(containers), 1)

    def test_can_get_container_infos(self):
        container_data = {
            "Name": "/mast__e45b0231-251f-401d-b379-eb5875fc343b",
            "Image": "sha256:2b8fd9751c4c0f5dd266fcae00707e67a2545ef34f9a29354585f93dac906749",
            "HostConfig": {
                "CpuShares": 0,
                "BlkioWeight": 0,
                "Privileged": False,
                "MemoryReservation": 0,
                "DnsOptions": None,
                "BlkioIOps": 0,
                "VolumeDriver": "",
                "BlkioDeviceReadIOps": None,
                "ExtraHosts": None,
                "OomKillDisable": False,
                "BlkioWeightDevice": None,
                "BlkioDeviceWriteIOps": None,
                "VolumesFrom": None,
                "UsernsMode": "",
                "Memory": 0,
                "Cgroup": "",
                "NetworkMode": "default",
                "PortBindings": None,
                "Devices": None,
                "RestartPolicy": {
                    "Name": "",
                    "MaximumRetryCount": 0
                },
                "StorageOpt": None,
                "KernelMemory": 0,
                "BlkioDeviceReadBps": None,
                "ReadonlyRootfs": False,
                "MemorySwappiness": -1,
                "ConsoleSize": [
                    0,
                    0
                ],
                "LogConfig": {
                    "Type": "json-file",
                    "Config": {}
                },
                "CapAdd": None,
                "CpusetCpus": "",
                "CpuPeriod": 0,
                "PublishAllPorts": False,
                "PidsLimit": 0,
                "SandboxSize": 0,
                "UTSMode": "",
                "PidMode": "",
                "ShmSize": 67108864,
                "AutoRemove": False,
                "Binds": None,
                "GroupAdd": None,
                "SecurityOpt": None,
                "MemorySwap": 0,
                "CpuQuota": 0,
                "Isolation": "",
                "OomScoreAdj": 0,
                "CpuPercent": 0,
                "CgroupParent": "",
                "DnsSearch": None,
                "CpusetMems": "",
                "Ulimits": None,
                "CpuCount": 0,
                "IpcMode": "",
                "CapDrop": None,
                "BlkioDeviceWriteBps": None,
                "ContainerIDFile": "",
                "DiskQuota": 0,
                "Links": None,
                "Dns": None,
                "BlkioBps": 0
            },
            "HostnamePath": "/var/lib/docker/containers/a5775b3cf95c465d5abcee59934c087cad9ca3d20bee266c44576b7b3d06ac1c/hostname",
            "GraphDriver": {
                "Name": "aufs",
                "Data": None
            },
            "ResolvConfPath": "/var/lib/docker/containers/a5775b3cf95c465d5abcee59934c087cad9ca3d20bee266c44576b7b3d06ac1c/resolv.conf",
            "Driver": "aufs",
            "LogPath": "/var/lib/docker/containers/a5775b3cf95c465d5abcee59934c087cad9ca3d20bee266c44576b7b3d06ac1c/a5775b3cf95c465d5abcee59934c087cad9ca3d20bee266c44576b7b3d06ac1c-json.log",
            "HostsPath": "/var/lib/docker/containers/a5775b3cf95c465d5abcee59934c087cad9ca3d20bee266c44576b7b3d06ac1c/hosts",
            "MountLabel": "",
            "State": {
                "Dead": False,
                "FinishedAt": "0001-01-01T00:00:00Z",
                "Restarting": False,
                "OOMKilled": False,
                "Running": True,
                "Status": "running",
                "StartedAt": "2016-06-30T11:39:49.527985338Z",
                "Paused": False,
                "ExitCode": 0,
                "Pid": 12209,
                "Error": ""
            },
            "Created": "2016-06-30T11:39:49.167801558Z",
            "ExecIDs": None,
            "Config": {
                "OpenStdin": False,
                "Image": "busybox:latest",
                "Volumes": None,
                "AttachStderr": True,
                "Env": [
                    "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
                ],
                "User": "",
                "Tty": False,
                "OnBuild": None,
                "AttachStdout": True,
                "Hostname": "a5775b3cf95c",
                "WorkingDir": "",
                "Labels": {},
                "Domainname": "",
                "Cmd": [
                    "tail",
                    "-f",
                    "/dev/None"
                ],
                "Entrypoint": None,
                "StdinOnce": False,
                "AttachStdin": False
            },
            "Args": [
                "-f",
                "/dev/None"
            ],
            "Path": "tail",
            "NetworkSettings": {
                "Networks": {
                    "bridge": {
                        "Aliases": None,
                        "MacAddress": "02:42:ac:11:00:04",
                        "EndpointID": "43d2052c35766a9b0f92608e0eeaa43b49a9194a3c7229be0834763ebe3d0276",
                        "IPAMConfig": None,
                        "GlobalIPv6Address": "",
                        "IPAddress": "172.17.0.4",
                        "Gateway": "172.17.0.1",
                        "Links": None,
                        "IPv6Gateway": "",
                        "NetworkID": "8a2d49200bc832dd80cefff90b60f29e0c8a4834db6af7f23006c94f6047a211",
                        "IPPrefixLen": 16,
                        "GlobalIPv6PrefixLen": 0
                    }
                },
                "MacAddress": "02:42:ac:11:00:04",
                "EndpointID": "43d2052c35766a9b0f92608e0eeaa43b49a9194a3c7229be0834763ebe3d0276",
                "GlobalIPv6Address": "",
                "SandboxKey": "/var/run/docker/netns/bb303663c5b4",
                "Gateway": "172.17.0.1",
                "HairpinMode": False,
                "SecondaryIPAddresses": None,
                "SecondaryIPv6Addresses": None,
                "LinkLocalIPv6PrefixLen": 0,
                "SandboxID": "bb303663c5b4d5b564cf9887609d0919145e95a8e56887a4c33701dea1da1ccb",
                "IPAddress": "172.17.0.4",
                "Ports": {},
                "Bridge": "",
                "IPPrefixLen": 16,
                "LinkLocalIPv6Address": "",
                "GlobalIPv6PrefixLen": 0,
                "IPv6Gateway": ""
            },
            "ProcessLabel": "",
            "Id": "a5775b3cf95c465d5abcee59934c087cad9ca3d20bee266c44576b7b3d06ac1c",
            "AppArmorProfile": "",
            "Mounts": [],
            "RestartCount": 0
        }

        infos = container_services.get_container_dict(container_data)
        self.assertDictEqual(infos, {'name': '/mast__e45b0231-251f-401d-b379-eb5875fc343b',
                                     'id': 'a5775b3cf95c465d5abcee59934c087cad9ca3d20bee266c44576b7b3d06ac1c',
                                     'status': 'running'}
                             )

    def test_can_destroy_container(self):
        self.skipTest('not implemented')

        # is it really helpful?
        # def test_pop_new_container(self):
        #     container = container_services.pop_new_container()
        #
        #     self.assertEqual(container.get('Warning'), None)
