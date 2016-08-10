import logging

import parser
import shell

logger = logging.getLogger(__name__)

daemon = '/etc/init.d/mast'
makefile = '/usr/sbin/mast-utils'


def add_printer(site, hostname, description=''):
    command = [makefile, 'add-channel',
               'NAME=' + site,
               'PRINTER=' + hostname,
               'DESC=' + description]
    response = shell.execute(command)
    response['results'] = parser.add_printer(response['results'])
    return response


def list_printers(site=''):
    command = [makefile, 'list-channels']
    if site:
        command.append(' NAME=' + site)

    response = shell.execute(command)
    response['results'] = parser.list_printers(response['results'], site)

    return response


def remove_printer(site, printer_id):
    command = [makefile, 'remove-channel',
               'ID=' + str(printer_id),
               'NAME=' + site
               ]
    return shell.execute(command)


def list_sites():
    command = [makefile, 'list-hosts']
    response = shell.execute(command)
    response['results'] = parser.list_sites(response['results'])
    return response


def add_site(name, hostname):
    command = [makefile, 'add-host',
               'NAME=' + name,
               'REMOTE_HOST=' + hostname,
               'INTERACTIVE=false'
               ]
    logger.debug(name, hostname, command)
    return shell.execute(command)


def remove_site(name):
    command = [makefile, 'remove-host', 'NAME=' + name]
    return shell.execute(command)


def get_printer(printers, id):
    for printer in printers:
        if printer['id'] == id:
            return printer