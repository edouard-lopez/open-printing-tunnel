import logging
from pprint import pprint

import paramiko

logger = logging.getLogger(__name__)


class Scanner:
    def __init__(self, network_tools, hostname):
        self.network_tools = network_tools
        self.hostname = hostname

    def scan(self, ports=9100, netmask=None):
        nmap = self.network_tools.nmap(target=self.hostname + netmask, ports=ports)
        details = self.get_details()
        return nmap

    def get_details(self):
        oids = [
            '.1.3.6.1.2.1.25.3.2.1.3.1',  # HOST-RESOURCES-MIB::hrDeviceDescr.1
            '.1.3.6.1.2.1.43.10.2.1.4.1.1'  # SNMPv2-SMI::mib-2.43.10.2.1.4.1.1 page count
            '.1.3.6.1.2.1.1.4.0',  # SNMPv2-MIB::sysContact.0
            '.1.3.6.1.2.1.1.1.0',  # SNMPv2-MIB::sysDescr.0
            '.1.3.6.1.2.1.1.5.0',  # SNMPv2-MIB::sysName.0
            '.1.3.6.1.2.1.1.3.0',  # DISMAN-EVENT-MIB::sysUpTimeInstance
        ]
        mibs = ['DISMAN-EVENT-MIB', 'HOST-RESOURCES-MIB', 'SNMPv2-MIB', 'SNMPv2-SMI']
        details = self.network_tools.snmp(self.hostname, oids, mibs)

        pprint(details)
        return {
            'description': details[0],
            'page_count': details[1],
            'sys_contact': details[2],
            'sys_description': details[3],
            'sys_name': details[4],
            'uptime': details[5],
        }

def fetch_netmask(hostname, port=22):
    private_key = '/home/mast/.ssh/id_rsa.mast.coaxis'
    connection = open_ssh_connection('coaxis', hostname, port=port, key=private_key)

    get_netmask = "ip -oneline -family inet address show | grep {}".format(hostname)
    stdin, stdout, stderr = connection.exec_command(get_netmask)
    logger.debug(stdout)
    address = parse_address(hostname, stdout)
    connection.close()

    return address

def open_ssh_connection(username, hostname, port=22, key=None):
    paramiko.util.log_to_file('/tmp/ssh.log')  # sets up logging
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port=port, timeout=0.3, username=username, key_filename=key)

    return client


def parse_address(hostname, addresses):
    netmask = ''

    for address in addresses:
        logger.debug(address)
        if hostname in address:
            _hostname, _netmask = address.strip().split('/')
            hostname = _hostname.split()[-1]
            netmask = '/' + _netmask.split()[0]
            break

    return netmask
