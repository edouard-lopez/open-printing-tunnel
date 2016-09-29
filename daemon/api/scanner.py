import nmap
import paramiko
from snimpy import manager as snimpy

from network_utils import logger


def scan(target, ports='9100'):
    scanner = nmap.PortScanner()

    return scanner.scan(hosts=target, ports=ports, arguments='-T5 --open')


def get_details(device):
    snimpy.load("SNMPv2-MIB")
    session = snimpy.snmp.Session("localhost", "public", 2)

    details = snimpy.Manager(device['hostname'])
    device_model = session.get("1.3.6.1.2.1.1.1.0")

    return {
        'contact': details.sysContact,  # SNMPv2-MIB
        'description': details.sysDescr,  # SNMPv2-MIB
        'hostname': device['hostname'],
        'name': details.sysName,  # SNMPv2-MIB
        'port': 9100,
        'uptime': details.sysUpTime,  # SNMPv2-MIB
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
    for address in addresses:
        logger.debug(address)
        if hostname in address:
            _hostname, _netmask = address.strip().split('/')
            hostname = _hostname.split()[-1]
            netmask = _netmask.split()[0]

            return '/' + netmask

    return None
