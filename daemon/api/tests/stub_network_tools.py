class NetworkToolsStub:
    def nmap(self, target, ports):
        return {
            'scan': {
                '10.0.1.250': {
                    'vendor': {},
                    'tcp': {9100: {
                        'state': 'open',
                        'product': '', 'version': '', 'reason': 'syn-ack', 'name': 'jetdirect',
                        'extrainfo': '', 'conf': '3', 'cpe': ''}},
                    'status': {'state': 'up', 'reason': 'syn-ack'},
                    'addresses': {'ipv4': '10.0.1.250'},
                    'hostnames': [{'type': '', 'name': ''}]},
                '10.0.1.248': {
                    'vendor': {},
                    'tcp': {9100: {
                        'state': 'open', 'product': '', 'version': '', 'reason': 'syn-ack',
                        'name': 'jetdirect', 'extrainfo': '', 'conf': '3', 'cpe': ''}},
                    'status': {'state': 'up', 'reason': 'conn-refused'},
                    'addresses': {'ipv4': '10.0.1.248'},
                    'hostnames': [{'type': '', 'name': ''}]}
            },
            'nmap': {
                'scanstats': {
                    'downhosts': '231', 'timestr': 'Thu Sep 29 17:58:46 2016', 'uphosts': '25',
                    'totalhosts': '256', 'elapsed': '2.27'
                },
                'command_line': 'nmap -oX - -p 9100 -T3 --open 10.0.1.231/24',
                'scaninfo': {
                    'tcp': {'services': '9100', 'method': 'connect'}}
            }
        }

    def snmp(self, hostname, oids, mibs):
        return [
            {'oid': '.1.3.6.1.2.1.25.3.2.1.3.1', 'value': 'Brother HL-5250DN series'},
            {'oid': '.1.3.6.1.2.1.1.4.0', 'value': ''},
            {'oid': '.1.3.6.1.2.1.1.1.0', 'value': 'Brother NC-6400h, Firmware Ver.1.01  (05.08.31),MID 84UZ92'},
            {'oid': '.1.3.6.1.2.1.1.5.0', 'value': 'BRN_7D3B43'},
            {'oid': '.1.3.6.1.2.1.1.3.0', 'value': 143431460},
            {'oid': '.1.3.6.1.2.1.43.10.2.1.4.1.1', 'value': 22625}
        ]

    def get_network_interfaces(self, hostname):
        return [
            "1: lo    inet 127.0.0.1/8 scope host lo\       valid_lft forever preferred_lft forever",
            "3: wlp4s0    inet 10.0.1.133/24 brd 10.0.1.255 scope global dynamic wlp4s0\       valid_lft 58984sec preferred_lft 58984sec",
            "4: docker0    inet 172.17.0.1/16 scope global docker0\       valid_lft forever preferred_lft forever",
            "5: br-a49026d1a341    inet 172.18.0.1/16 scope global br-a49026d1a341\       valid_lft forever preferred_lft forever",
            "6: br-d26f2005f732    inet 172.19.0.1/16 scope global br-d26f2005f732\       valid_lft forever preferred_lft forever",
        ]
