from api import shell


class Service(object):
    def __init__(self):
        self.program = '/etc/init.d/mast'

    def add_host(self, name, remote_host):
        return shell.execute([self.program, name, remote_host])


class Makefile(object):
    def __init__(self):
        self.makefile = '/usr/sbin/mast-utils'
