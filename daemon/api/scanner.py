import logging

logger = logging.getLogger(__name__)


class Scanner:
    def __init__(self, network_tools, hostname):
        self.network_tools = network_tools
        self.hostname = hostname

    def scan(self, port='9100'):
        target = self.hostname + self.get_netmask()

        logger.debug('target');
        logger.debug(target)
        nmap = self.clean_nmap(self.network_tools.nmap(target=target, ports=str(port)))
        nmap_snmp = self.add_snmp_infos(nmap)
        return nmap_snmp

    def get_netmask(self):
        addresses = self.network_tools.get_network_interfaces(self.hostname)

        return self.parse_address(addresses)

    def parse_address(self, addresses):
        netmask = ''

        for address in addresses:
            logger.debug(address)
            if self.hostname in address:
                _hostname, _netmask = address.strip().split('/')
                hostname = _hostname.split()[-1]
                netmask = '/' + _netmask.split()[0]
                break

        return netmask

    def clean_nmap(self, nmap):
        devices = {}

        for (device, device_details) in nmap['scan'].items():
            devices[device] = {}
            for (port, port_details) in device_details['tcp'].items():
                devices[device][str(port)] = {'open': port_details['state'] == 'open'}

        return {
            'raw': nmap['nmap']['command_line'],
            'devices': devices
        }

    def get_device_infos(self, hostname):
        oids = [
            '.1.3.6.1.2.1.25.3.2.1.3.1',  # HOST-RESOURCES-MIB::hrDeviceDescr.1
            '.1.3.6.1.2.1.1.4.0',  # SNMPv2-MIB::sysContact.0
            '.1.3.6.1.2.1.1.1.0',  # SNMPv2-MIB::sysDescr.0
            '.1.3.6.1.2.1.1.5.0',  # SNMPv2-MIB::sysName.0
            '.1.3.6.1.2.1.1.3.0',  # DISMAN-EVENT-MIB::sysUpTimeInstance
            # fixme: must be last otherwise break function o__O
            '.1.3.6.1.2.1.43.10.2.1.4.1.1'  # SNMPv2-SMI::mib-2.43.10.2.1.4.1.1 page count
        ]
        mibs = ['DISMAN-EVENT-MIB', 'HOST-RESOURCES-MIB', 'SNMPv2-MIB', 'SNMPv2-SMI']
        infos = self.network_tools.snmp(hostname, oids, mibs)

        return {
            'description': infos[0],
            'page_count': infos[1],
            'sys_contact': infos[2],
            'sys_description': infos[3],
            'sys_name': infos[4],
            'uptime': infos[5],
        }

    def add_snmp_infos(self, nmap):
        for (device, data) in nmap['devices'].items():
            logger.debug(device)
            logger.debug(data)
            infos = self.get_device_infos(device)
            nmap['devices'][device].update(infos)

        return nmap
