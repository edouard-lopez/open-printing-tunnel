mock_daemon_container_data = {
    "Id": "9cd8fc43d68b6245b66a3ab2b016d76ef672f844579ee84695f141289e57a569",
    "Created": "2017-02-27T14:08:10.241186136Z",
    "Path": "/usr/bin/supervisord",
    "Args": [
        "-c",
        "/etc/supervisor/conf.d/prod.conf"
    ],
    "State": {
        "Status": "running",
        "Running": True,
        "Paused": False,
        "Restarting": False,
        "OOMKilled": False,
        "Dead": False,
        "Pid": 14551,
        "ExitCode": 0,
        "Error": "",
        "StartedAt": "2017-02-27T14:08:10.950585898Z",
        "FinishedAt": "0001-01-01T00:00:00Z"
    },
    "Image": "sha256:b3082447f19289f4b95b40db7620d837e313dd543db53bd9021e2564763ba9e7",
    "ResolvConfPath": "/var/lib/docker/containers/9cd8fc43d68b6245b66a3ab2b016d76ef672f844579ee84695f141289e57a569/resolv.conf",
    "HostnamePath": "/var/lib/docker/containers/9cd8fc43d68b6245b66a3ab2b016d76ef672f844579ee84695f141289e57a569/hostname",
    "HostsPath": "/var/lib/docker/containers/9cd8fc43d68b6245b66a3ab2b016d76ef672f844579ee84695f141289e57a569/hosts",
    "LogPath": "/var/lib/docker/containers/9cd8fc43d68b6245b66a3ab2b016d76ef672f844579ee84695f141289e57a569/9cd8fc43d68b6245b66a3ab2b016d76ef672f844579ee84695f141289e57a569-json.log",
    "Name": "/priceless_jepsen",
    "RestartCount": 0,
    "Driver": "aufs",
    "MountLabel": "",
    "ProcessLabel": "",
    "AppArmorProfile": "",
    "ExecIDs": None,
    "HostConfig": {
        "Binds": None,
        "ContainerIDFile": "",
        "LogConfig": {
            "Type": "json-file",
            "Config": {}
        },
        "NetworkMode": "default",
        "PortBindings": {
            "80/tcp": [
                {
                    "HostIp": "",
                    "HostPort": "80"
                }
            ]
        },
        "RestartPolicy": {
            "Name": "always",
            "MaximumRetryCount": 0
        },
        "AutoRemove": False,
        "VolumeDriver": "",
        "VolumesFrom": None,
        "CapAdd": None,
        "CapDrop": None,
        "Dns": None,
        "DnsOptions": None,
        "DnsSearch": None,
        "ExtraHosts": None,
        "GroupAdd": None,
        "IpcMode": "",
        "Cgroup": "",
        "Links": None,
        "OomScoreAdj": 0,
        "PidMode": "",
        "Privileged": False,
        "PublishAllPorts": False,
        "ReadonlyRootfs": False,
        "SecurityOpt": None,
        "UTSMode": "",
        "UsernsMode": "",
        "ShmSize": 67108864,
        "Runtime": "runc",
        "ConsoleSize": [
            0,
            0
        ],
        "Isolation": "",
        "CpuShares": 0,
        "Memory": 0,
        "NanoCpus": 0,
        "CgroupParent": "",
        "BlkioWeight": 0,
        "BlkioWeightDevice": None,
        "BlkioDeviceReadBps": None,
        "BlkioDeviceWriteBps": None,
        "BlkioDeviceReadIOps": None,
        "BlkioDeviceWriteIOps": None,
        "CpuPeriod": 0,
        "CpuQuota": 0,
        "CpuRealtimePeriod": 0,
        "CpuRealtimeRuntime": 0,
        "CpusetCpus": "",
        "CpusetMems": "",
        "Devices": None,
        "DiskQuota": 0,
        "KernelMemory": 0,
        "MemoryReservation": 0,
        "MemorySwap": 0,
        "MemorySwappiness": -1,
        "OomKillDisable": False,
        "PidsLimit": 0,
        "Ulimits": None,
        "CpuCount": 0,
        "CpuPercent": 0,
        "IOMaximumIOps": 0,
        "IOMaximumBandwidth": 0
    },
    "GraphDriver": {
        "Name": "aufs",
        "Data": None
    },
    "Mounts": [
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
    ],
    "Config": {
        "Hostname": "test-01",
        "Domainname": "",
        "User": "",
        "AttachStdin": False,
        "AttachStdout": True,
        "AttachStderr": True,
        "ExposedPorts": {
            "5000/tcp": {},
            "80/tcp": {},
            "8080/tcp": {}
        },
        "Tty": False,
        "OpenStdin": False,
        "StdinOnce": False,
        "Env": [
            "PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
            "LANG=C.UTF-8",
            "GPG_KEY=97FC712E4C024BBEA48A61ED3A5CA953F73C700D",
            "PYTHON_VERSION=3.5.2",
            "PYTHON_PIP_VERSION=8.1.2",
            "TERM=linux",
            "DEBIAN_FRONTEND=noninteractive",
            "NPM_CONFIG_LOGLEVEL=info",
            "NODE_VERSION=4.4.7"
        ],
        "Cmd": [
            "/usr/bin/supervisord",
            "-c",
            "/etc/supervisor/conf.d/prod.conf"
        ],
        "ArgsEscaped": True,
        "Image": "docker.akema.fr:5000/coaxis/coaxisopt_daemon:latest",
        "Volumes": {
            "/etc/mast": {},
            "/home/mast/.ssh": {}
        },
        "WorkingDir": "/frontend",
        "Entrypoint": None,
        "OnBuild": None,
        "Labels": {}
    },
    "NetworkSettings": {
        "Bridge": "",
        "SandboxID": "f0599cfd466007d491297116b8d492bf17c756a4f4d3cd2bbc16a2e2af96c27e",
        "HairpinMode": False,
        "LinkLocalIPv6Address": "",
        "LinkLocalIPv6PrefixLen": 0,
        "Ports": {},
        "SandboxKey": "/var/run/docker/netns/f0599cfd4660",
        "SecondaryIPAddresses": None,
        "SecondaryIPv6Addresses": None,
        "EndpointID": "",
        "Gateway": "",
        "GlobalIPv6Address": "",
        "GlobalIPv6PrefixLen": 0,
        "IPAddress": "",
        "IPPrefixLen": 0,
        "IPv6Gateway": "",
        "MacAddress": "",
        "Networks": {
            "opt_network_508be7": {
                "IPAMConfig": {
                    "IPv4Address": "10.0.0.1"
                },
                "Links": None,
                "Aliases": [
                    "9cd8fc43d68b"
                ],
                "NetworkID": "f9ea8770daced81505bd053d98b84efb4e714ed2430cbf12b5dddb677a4d852a",
                "EndpointID": "980562393a101e5e21a5370ec27902a98c91b3fd4520695a71b2baa1e8ecde12",
                "Gateway": "10.0.0.254",
                "IPAddress": "10.0.0.1",
                "IPPrefixLen": 24,
                "IPv6Gateway": "",
                "GlobalIPv6Address": "",
                "GlobalIPv6PrefixLen": 0,
                "MacAddress": "02:42:0a:00:00:01"
            }
        }
    }
}

mock_images = [
    {
        'Id': 'sha256:6003ceb6aaf35c9df4e21bd57266553e7b9f2077d5ebd21a0cef28c3d8ca066f',
        'RepoTags': ['coaxisopt_backend:latest']
    },
    {
        'Id': 'sha256:399c8c2886ef189bee63f62767d56063ba24eb79cf9f04da78d088e4426cc328',
        'RepoTags': ['coaxisopt_daemon:latest']
    },
    {
        'Id': 'sha256:3e3a33a8e8f930a923545c2ab2abb0f233e9a44ca83e3609697cd2dbf67a0645',
        'RepoTags': ['colstrom/fish:latest']
    },
    {
        'Id': 'sha256:b8a28fa9fa9c7b921af486a23f89862de7616ade4c424b351e779b3e2436e4a6',
        'RepoTags': ['docker.akema.fr:5000/coaxis/coaxisopt_daemon:latest']
    },
    {
        'Id': 'sha256:652e925c18f391e28ef88c7bfc7ca617daaa4152cc99583f3d57ac7d31dd279b',
        'RepoTags': ['docker.akema.fr:5000/coaxis/coaxisopt_daemon:v1.6.1']
    },
    {
        'Id': 'sha256:d8f4b42c0cae4629b1d2db815900a6bfc58c211518d16d01496f09b0057ecb56',
        'RepoTags': ['docker.akema.fr:5000/coaxis/coaxisopt_backend:v1.6.1']
    },
    {
        'Id': 'sha256:e6cff3d768d43bb5fe70d9b59a5815eb66b5225bfa341bc9259a66d5976499c5',
        'RepoTags': ['docker.akema.fr:5000/coaxis/coaxisopt_daemon:v1.6.0']
    },
    {
        'Id': 'sha256:239ea3f40e72f42b7d053e70abde0239b1b9b22b1f2f7a37545db5a64b2129b2',
        'RepoTags': ['coaxisopt_frontend:latest',
                     'docker.akema.fr:5000/coaxis/coaxisopt_frontend:latest',
                     'docker.akema.fr:5000/coaxis/coaxisopt_frontend:v1.6.0',
                     'docker.akema.fr:5000/coaxis/coaxisopt_frontend:v1.6.1']
    },
    {
        'Id': 'sha256:00541b7f7424a504441133132da0b4b3948c8448c365874a1089e1be4563c750',
        'RepoDigests': ['node@sha256:460bbe8965aceb8d7c78d0d7d9366170afb40949a20cec592a48a42a5addd313'],
        'RepoTags': ['node:argon-slim']
    }
]


def get_one_container_data():
    return mock_daemon_container_data


def get_images():
    return mock_images
