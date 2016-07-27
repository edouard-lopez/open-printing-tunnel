from slugify import slugify

from api import shell
from api import validators


class Daemon(object):
    program = '/etc/init.d/mast'

    def add_host(self, name, remote_host):
        name = slugify(name)
        if validators.is_valid_host(remote_host):
            return shell.execute([Daemon.program, name, remote_host])
        else:
            raise ValueError


class Utils(object):
    program = '/usr/sbin/mast-utils'

    @classmethod
    def list_hosts(cls):
        return shell.execute([Utils.program, 'list-hosts'])
