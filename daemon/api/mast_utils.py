import logging

import parser
import shell

logger = logging.getLogger(__name__)

daemon = '/etc/init.d/mast'
makefile = '/usr/sbin/mast-utils'


def add_printer(name, hostname, description=''):
    command = [makefile, 'add-channel', 'NAME=' + name, 'PRINTER=' + hostname, 'DESC=' + description]
    return shell.execute(command)


def list_printers(name=''):
    command = [makefile, 'list-channels']
    if name:
        command.append(' NAME=' + name)

    response = shell.execute(command)
    response['output'] = parser.list_printers(response['output'], name)

    return response


def remove_printer(id, name):
    command = [makefile, 'remove-channel', 'ID=' + id, 'NAME=' + name]
    return shell.execute(command)


def list_optboxes():
    command = [makefile, 'list-hosts']
    response = shell.execute(command)
    response['output'] = parser.list_optboxes(response['output'])
    return response


def add_optbox(name, hostname):
    command = [makefile, 'add-host', 'NAME=' + name, 'REMOTE_HOST=' + hostname]
    logger.debug(name, hostname, command)
    return shell.execute(command)


def remove_optbox(name):
    command = [makefile, 'remove-host', 'NAME=' + name]
    return shell.execute(command)
