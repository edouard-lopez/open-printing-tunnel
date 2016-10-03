import logging

import nmap
import paramiko
from snimpy import manager as snimpy

logger = logging.getLogger(__name__)


class NetworkTools:
    def nmap(self, target, ports):
        scanner = nmap.PortScanner()

        return scanner.scan(hosts=target, ports=ports, arguments='-T5 --open')

    def snmp(self, hostname, oids, mibs):
        for mib in mibs:
            snimpy.load(mib)
        session = snimpy.snmp.Session(hostname, "public", 1)

        details = [{
                       'oid': '.' + '.'.join(repr(node) for node in oid[0]),
                       'value': oid[1]
                   } for oid in oids]    def open_ssh_connection(self, username, hostname, port=22):
    def open_ssh_connection(self, username, hostname, port=22):
        paramiko.util.log_to_file('/tmp/ssh.log')  # sets up logging
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=port, timeout=0.3, username=username, key_filename=self.private_key)

        return client

