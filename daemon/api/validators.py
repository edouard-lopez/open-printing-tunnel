import ipaddress
import re

IP_ADDRESS_REGEX = r'^25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$'  # use in other regexp do NOT modify
NAME_REGEX = r'[a-zA-Z0-9_:\-]+'
HOSTNAME_REGEX = r'(((^|\.)((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]?\d))){4}$)|(^([a-zA-Z]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$)'
DESCRIPTION_REGEX = r'[a-zA-Z0-9_:\-\(\)\[\]\{\}><\.\s]{3,40}'


def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def is_valid_host(host):
    return is_valid_ip(host) or bool(re.match(HOSTNAME_REGEX, host))
