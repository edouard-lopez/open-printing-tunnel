import logging

import parser
import shell

logger = logging.getLogger(__name__)

daemon = '/etc/init.d/mast'


def service(action, name):
    return shell.execute([daemon, action, name])


def restart(name):
    return service('restart', name)


def start(name):
    return service('start', name)


def status(name):
    response = service('status', name)
    response['output'] = parser.status(response['output'])
    return response


def stop(name):
    return service('stop', name)
