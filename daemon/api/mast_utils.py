import logging

import shell

logger = logging.getLogger(__name__)

daemon = '/etc/init.d/mast'
makefile = '/usr/sbin/mast-utils'


# [key + '=' + o[key] for key in o]


def add_channel(name, hostname, description=''):
    command = [makefile, 'add-channel', 'NAME=' + name, 'PRINTER=' + hostname, 'DESC=' + description]
    return shell.execute(command)


def list_channels(name=''):
    command = [makefile, 'list-channels']
    if name:
        command.append('NAME=' + name)
    return shell.execute(command)


def remove_channel(id, name):
    command = [makefile, 'remove-channel', 'ID=' + id, 'NAME=' + name]
    return shell.execute(command)


def list_hosts():
    command = [makefile, 'list-hosts']
    return shell.execute(command)


def add_host(name, hostname):
    command = [makefile, 'add-host', 'NAME=' + name, 'REMOTE_HOST=' + hostname]
    return shell.execute(command)


def remove_host(name):
    command = [makefile, 'remove-host', 'NAME=' + name]
    return shell.execute(command)
