import logging

import parser
import shell

logger = logging.getLogger(__name__)

daemon = '/etc/init.d/mast'
makefile = '/usr/sbin/mast-utils'


def add_printer(optbox, hostname, description=''):
    command = [makefile, 'add-channel',
               'NAME=' + optbox,
               'PRINTER=' + hostname,
               'DESC=' + description]
    response = shell.execute(command)
    response['output'] = parser.add_printer(response['output'])
    return response


def list_printers(optbox=''):
    command = [makefile, 'list-channels']
    if optbox:
        command.append(' NAME=' + optbox)

    response = shell.execute(command)
    response['output'] = parser.list_printers(response['output'], optbox)

    return response


def remove_printer(optbox, printer_id):
    command = [makefile, 'remove-channel',
               'ID=' + str(printer_id),
               'NAME=' + optbox
               ]
    return shell.execute(command)


def list_sites():
    command = [makefile, 'list-hosts']
    response = shell.execute(command)
    response['output'] = parser.list_sites(response['output'])
    return response


def add_optbox(name, hostname):
    command = [makefile, 'add-host',
               'NAME=' + name,
               'REMOTE_HOST=' + hostname,
               'INTERACTIVE=false'
               ]
    logger.debug(name, hostname, command)
    return shell.execute(command)


def remove_optbox(name):
    command = [makefile, 'remove-host', 'NAME=' + name]
    return shell.execute(command)


def get_printer(printers, id):
    for printer in printers:
        if printer['id'] == id:
            return printer