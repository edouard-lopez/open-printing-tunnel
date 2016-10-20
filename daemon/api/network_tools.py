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

        logger.debug('nmap {} -p {} -T3 --open'.format(target, ports))
        return scanner.scan(hosts=target, ports=ports, arguments='-T3 --open')

    @staticmethod
    def snmp(hostname, oids, mibs):
        logger.debug(hostname); logger.debug(oids); logger.debug(mibs)
        for mib in mibs:
            snimpy.load(mib)

        try:
            session = snimpy.snmp.Session(hostname, "public", 1)
            session.timeout = 300  # ms
            session.retries = 2
            infos = session.get(*oids)
            snmp_results = NetworkTools.format_snmp_results(infos)
        except:
            snmp_results = NetworkTools.format_empty_result(oids)

        return snmp_results

    @staticmethod
    def format_empty_result(oids):
        return [{'oid': oid, 'value': None} for oid in oids]

    @staticmethod
    def format_snmp_results(details):
        results = []

        for path, value in details:
            oid = '.' + '.'.join(repr(node) for node in path)
            value = value.decode('utf-8') if type(value) == bytes else value

            results.append({
                'oid': oid,
                'value': value
            })

        return results

    def open_ssh_connection(self, username, hostname, port=22):
        paramiko.util.log_to_file('/tmp/ssh.log')  # sets up logging
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=port, timeout=0.3, username=username, key_filename=self.private_key)

        return client

    def get_network_interfaces(self, hostname, username='coaxis'):
        connection = self.open_ssh_connection(username, hostname)

        logger.debug('connecting on: ' + hostname)
        network_devices = "ip -oneline -family inet address show | grep {}".format(hostname)
        logger.debug(network_devices)

        stdin, stdout, stderr = connection.exec_command(network_devices)

        stdout.channel.recv_exit_status()
        logger.debug(stdout)
        connection.close()

        return stdout
