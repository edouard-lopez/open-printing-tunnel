import logging

import nmap
import paramiko
from snimpy import manager as snimpy

logger = logging.getLogger(__name__)


class NetworkTools:
    def __init__(self, private_key='/home/mast/.ssh/id_rsa.mast.coaxis'):
        self.private_key = private_key

    @staticmethod
    def nmap(target, ports):
        scanner = nmap.PortScanner()

        return scanner.scan(hosts=target, ports=ports, arguments='-T5 --open')

    @staticmethod
    def snmp(hostname, oids, mibs):
        for mib in mibs:
            snimpy.load(mib)

        session = snimpy.snmp.Session(hostname, "public", 1)
        details = session.get(*oids)
        logger.debug(oids)

        return [{
                       'oid': '.' + '.'.join(repr(node) for node in oid[0]),
                       'value': oid[1]
                   } for oid in details]

    def open_ssh_connection(self, username, hostname, port=22):
        paramiko.util.log_to_file('/tmp/ssh.log')  # sets up logging
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=port, timeout=0.3, username=username, key_filename=self.private_key)

        return client

    def get_network_interfaces(self, hostname):
        connection = self.open_ssh_connection('coaxis', hostname)

        logger.debug('connecting on: ' + hostname)
        network_devices = "ip -oneline -family inet address show | grep {}".format(hostname)
        logger.debug(network_devices)

        stdin, stdout, stderr = connection.exec_command(network_devices)

        stdout.channel.recv_exit_status()
        logger.debug(stdout)
        connection.close()

        return stdout
