import logging
import socket
import threading

import os
import nmap
import paramiko
import snimpy.manager as snimpy

import output_parser
import shell

logger = logging.getLogger(__name__)


def fping(hostnames):
    command = ['fping',
               '-p', '100',
               '-r', '0',
               '-t', '300',
               '-e',
               ]
    command.extend(hostnames)

    response = shell.execute(command)

    return output_parser.fping(response['results'])


def telnet(hostname=None, port=22, timeout=0.3, **kwargs):
    logger.debug('telnet: {}:{}'.format(hostname, port))
    connection = socket.socket()
    connection.settimeout(timeout)
    try:
        connection.connect((hostname, port))
        reachable = True
    except:
        reachable = False
    finally:
        connection.close()

    return {'telnet': reachable}


def collect(task, response, **kwargs):
    hostname = kwargs['hostname']

    response[hostname] = task(**kwargs)


def parellelize(task, site_id, printers, **kwargs):
    response = {}
    kw = kwargs.copy()
    kw.update({'hostname': site_id})
    collect(task, response, **kw)

    printers_response = {}
    threads = []
    for printer in printers:
        kw = kwargs.copy()
        kw.update({
            'hostname': (printer['hostname']),
            'port': (printer['ports']['send'])
        })

        thread = threading.Thread(target=collect, args=(task, printers_response), kwargs=kw)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    response[site_id].update(printers_response)

    return response


def ping_site_and_printers(site_hostname, printers):
    hostnames = [site_hostname]
    printers_hostnames = [printer['hostname'] for printer in printers]

    response = fping([site_hostname])
    if len(printers_hostnames) > 0:
        response[site_hostname].update(fping(printers_hostnames))

    return response


def deep_merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                deep_merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


def scan(target, ports='9100'):
    scanner = nmap.PortScanner()

    scan = scanner.scan(hosts=target, ports=ports, arguments='-T5 --open')

    return scan


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

    get_netmask = ("ip -oneline -family inet address show | grep {}").format(hostname)
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
            hostname, netmask = address.strip().split('/')
            hostname = hostname.split()[-1]
            netmask = netmask.split()[0]

            return '/' + netmask

    return None
