import logging

import parser
import shell

logger = logging.getLogger(__name__)

daemon = '/etc/init.d/mast'


def service(action, name):
    response = shell.execute([daemon, action, name])
    response['results'] = getattr(parser, action)(response['results'])
    return response


def restart(name):
    return service('restart', name)


def start(name):
    return service('start', name)


def status(name):
    return service('status', name)


def stop(name):
    return service('stop', name)
