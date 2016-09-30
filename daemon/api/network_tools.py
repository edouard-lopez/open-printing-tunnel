import nmap
from snimpy import manager as snimpy


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
                   } for oid in oids]