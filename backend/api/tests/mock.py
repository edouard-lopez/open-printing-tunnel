mock_container_data = {
    'ProcessLabel': '',
    'Id': '21e9f7f57aa2b619f259ab3995d0174d107f0fc5d6349b3f7ca581cd185a9e57',
    'LogPath': '/var/lib/docker/containers/21e9f7f57aa2b619f259ab3995d0174d107f0fc5d6349b3f7ca581cd185a9e57/21e9f7f57aa2b619f259ab3995d0174d107f0fc5d6349b3f7ca581cd185a9e57-json.log',
    'Created': '2016-07-28T16:06:18.085698135Z',
    'ResolvConfPath': '/var/lib/docker/containers/21e9f7f57aa2b619f259ab3995d0174d107f0fc5d6349b3f7ca581cd185a9e57/resolv.conf',
    'AppArmorProfile': '',
    'Driver': 'aufs',
    'Mounts': [],
    'HostsPath': '/var/lib/docker/containers/21e9f7f57aa2b619f259ab3995d0174d107f0fc5d6349b3f7ca581cd185a9e57/hosts',
    'HostConfig': {
        'Privileged': False,
        'LogConfig': {
            'Type': 'json-file',
            'Config': {}},
        'IpcMode': '',
        'Ulimits': None,
        'OomScoreAdj': 0,
        'ContainerIDFile': '',
        'CapAdd': None,
        'BlkioIOps': 0,
        'BlkioBps': 0,
        'CpusetCpus': '',
        'MemoryReservation': 0,
        'CgroupParent': '',
        'VolumeDriver': '',
        'CpuCount': 0,
        'Memory': 0,
        'BlkioDeviceReadBps': None,
        'Links': None,
        'KernelMemory': 0,
        'BlkioDeviceWriteIOps': None,
        'DnsSearch': None,
        'SecurityOpt': None,
        'RestartPolicy': {
            'MaximumRetryCount': 0,
            'Name': ''},
        'DnsOptions': None,
        'OomKillDisable': False,
        'GroupAdd': None,
        'Cgroup': '',
        'ShmSize': 67108864,
        'ExtraHosts': None,
        'PublishAllPorts': False,
        'PortBindings': None,
        'BlkioWeight': 0,
        'MemorySwap': 0,
        'DiskQuota': 0,
        'AutoRemove': False,
        'Devices': None,
        'CpusetMems': '',
        'Binds': None,
        'PidsLimit': 0,
        'CpuPeriod': 0,
        'ReadonlyRootfs': False,
        'CpuShares': 0,
        'NetworkMode': 'default',
        'BlkioWeightDevice': None,
        'UTSMode': '',
        'VolumesFrom': None,
        'Isolation': '',
        'Dns': None,
        'SandboxSize': 0,
        'CpuPercent': 0,
        'ConsoleSize': [0, 0],
        'StorageOpt': None,
        'CpuQuota': 0,
        'MemorySwappiness': -1,
        'UsernsMode': '',
        'BlkioDeviceReadIOps': None,
        'BlkioDeviceWriteBps': None,
        'PidMode': '',
        'CapDrop': None},
    'RestartCount': 0,
    'ExecIDs': None,
    'MountLabel': '',
    'Image': 'sha256:0627e0366ef8ce8dd249f518fdcd19d9f5d3d69910fa869f645032bbb16f5281',
    'State': {
        'OOMKilled': False,
        'Restarting': False,
        'StartedAt': '2016-07-28T16:06:18.382183467Z',
        'Status': 'running',
        'Dead': False,
        'Running': True,
        'Pid': 3351,
        'Error': '',
        'ExitCode': 0,
        'FinishedAt': '0001-01-01T00:00:00Z',
        'Paused': False},
    'NetworkSettings': {
        'LinkLocalIPv6Address': '',
        'EndpointID': '',
        'SecondaryIPv6Addresses': None,
        'GlobalIPv6Address': '',
        'SecondaryIPAddresses': None,
        'MacAddress': '',
        'Ports': {
            '443/tcp': None,
            '80/tcp': None,
            '5000/tcp': None},
        'Networks': {
            'opt_network_0d8dbb': {
                'EndpointID': '77bdd95fb5fdee829cbdc8eea1b7881ab51937de0de86117300fa48a121ef9bc',
                'GlobalIPv6Address': '',
                'NetworkID': '17a286794ae276382b8e76d5ab7f4dce3f7eccf3445e2251eae888df7b2b3b06',
                'MacAddress': '02:42:0a:00:00:02',
                'Links': None,
                'IPv6Gateway': '',
                'Gateway': '10.0.0.1',
                'IPPrefixLen': 24,
                'GlobalIPv6PrefixLen': 0,
                'IPAMConfig': None,
                'IPAddress': '10.0.0.2',
                'Aliases': None}},
        'HairpinMode': False,
        'LinkLocalIPv6PrefixLen': 0,
        'Bridge': '',
        'Gateway': '',
        'SandboxKey': '/var/run/docker/netns/46503f3ba4d4',
        'IPPrefixLen': 0,
        'GlobalIPv6PrefixLen': 0,
        'IPv6Gateway': '',
        'IPAddress': '',
        'SandboxID': '46503f3ba4d407866caf7f1b407ae58d26253221b6fdd1e35ae32d1365c79e04'},
    'Path': 'tail',
    'HostnamePath': '/var/lib/docker/containers/21e9f7f57aa2b619f259ab3995d0174d107f0fc5d6349b3f7ca581cd185a9e57/hostname',
    'Name': '/desperate_nobel',
    'GraphDriver': {
        'Data': None,
        'Name': 'aufs'},
    'Config': {
        'Labels': {},
        'OpenStdin': False,
        'User': '',
        'AttachStderr': True,
        'Volumes': None,
        'Env': [
            'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
            'LANG=C.UTF-8',
            'GPG_KEY=97FC712E4C024BBEA48A61ED3A5CA953F73C700D',
            'PYTHON_VERSION=3.5.2',
            'PYTHON_PIP_VERSION=8.1.2',
            'TERM=linux',
            'DEBIAN_FRONTEND=noninteractive'
        ],
        'Domainname': '',
        'AttachStdout': True,
        'Hostname': '21e9f7f57aa2',
        'WorkingDir': '/daemon',
        'ExposedPorts': {
            '443/tcp': {},
            '80/tcp': {},
            '5000/tcp': {}},
        'AttachStdin': False,
        'OnBuild': None,
        'Entrypoint': None,
        'Tty': False,
        'Image': 'coaxisopt_daemon',
        'StdinOnce': False,
        'Cmd': [
            'tail',
            '-f',
            '/dev/null'
        ]
    },
    'Args': [
        '-f',
        '/dev/null'
    ]
}


def get_one_container_data():
    return mock_container_data