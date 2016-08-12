import logging
import shlex

import output_parser
import shell

logger = logging.getLogger(__name__)

makefile = '/usr/sbin/mast-utils'


def add_printer(site, hostname, description=None):
    command = [makefile, 'add-channel',
               'NAME=' + site,
               'PRINTER=' + hostname,
               'DESC=' + shlex.quote(description)]
    response = shell.execute(command)
    response['results'] = output_parser.add_printer(response['results'])
    return response


def list_site_and_printers():
    command = [makefile, 'list-channels']

    response = shell.execute(command)
    response['results'] = output_parser.list_all_printers(response['results'])

    return response


def list_printers(site):
    command = [makefile, 'list-channels']
    if site:
        command.append(' NAME=' + site)

    response = shell.execute(command)
    response['results'] = output_parser.list_printers(response['results'], site)

    return response


def remove_printer(site, printer_id):
    command = [makefile, 'remove-channel',
               'NAME=' + site,
               'ID=' + str(printer_id)
               ]
    return shell.execute(command)


def list_sites():
    command = [makefile, 'list-hosts']
    response = shell.execute(command)
    response['results'] = output_parser.list_sites(response['results'])
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
