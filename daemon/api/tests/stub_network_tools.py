class NetworkToolsStub:
    def nmap(self, target, ports):
        return {'scan': {
            '192.168.2.250': {
                'vendor': {},
                'tcp': {9100: {
                    'state': 'open',
                    'product': '', 'version': '', 'reason': 'syn-ack', 'name': 'jetdirect',
                    'extrainfo': '', 'conf': '3', 'cpe': ''}},
                'status': {'state': 'up', 'reason': 'syn-ack'},
                'addresses': {'ipv4': '192.168.2.250'},
                'hostnames': [{'type': '', 'name': ''}]},
            '192.168.2.248': {
                'vendor': {},
                'tcp': {9100: {
                    'state': 'open', 'product': '', 'version': '', 'reason': 'syn-ack',
                    'name': 'jetdirect', 'extrainfo': '', 'conf': '3', 'cpe': ''}},
                'status': {'state': 'up', 'reason': 'conn-refused'},
                'addresses': {'ipv4': '192.168.2.248'},
                'hostnames': [{'type': '', 'name': ''}]}
        },
            'nmap': {
                'scanstats': {
                    'downhosts': '231', 'timestr': 'Thu Sep 29 17:58:46 2016', 'uphosts': '25',
                    'totalhosts': '256', 'elapsed': '2.27'
                },
                'command_line': 'nmap -oX - -p 9100 -T5 --open 192.168.2.231/24',
                'scaninfo': {
                    'tcp': {'services': '9100', 'method': 'connect'}}
            }
        }

    def snmp(self, hostname, oids, mibs):
        return [
            {'oid': '.1.3.6.1.2.1.1.5.0', 'value': b'BRN_7D3B43'},
            {'oid': '.1.3.6.1.2.1.1.3.0', 'value': 143431460},
            {'oid': '.1.3.6.1.2.1.25.3.2.1.3.1', 'value': b'Brother HL-5250DN series'},
            {'oid': '.1.3.6.1.2.1.1.1.0',
             'value': b'Brother NC-6400h, Firmware Ver.1.01  (05.08.31),MID 84UZ92'},
            {'oid': '.1.3.6.1.2.1.1.4.0', 'value': b''},
            {'oid': '.1.3.6.1.2.1.43.10.2.1.4.1.1', 'value': 22625}
        ]
