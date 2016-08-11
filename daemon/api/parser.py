import logging
import re

logger = logging.getLogger(__name__)


def list_sites(lines):
    parser = re.compile(r'[\s]*(?P<id>[^\s]+)[\s]*(?P<hostname>[^\n\t]+)')
    response = []
    for line in lines:
        data = parser.search(line).groupdict()
        response.append({
            'id': data['id'],
            'hostname': data['hostname'],
        })

    return response


def status(lines, id=None):
    response = []

    for line in lines:
        state = detect_status_state(line)
        if state == 'on':
            response = status_is_on(lines)
        elif state == 'off':
            response = status_is_off(lines)

    return response

def detect_status_state(line):
    parser = re.compile(r'\s*(?P<state>on(?=\s+pid)|off(?=\s+))')

    data = parser.search(line).groupdict()
    state = data['state']
    return state


def status_is_on(lines):
    parser = re.compile(
        r'\s*(?P<id>\w+):autossh\s+(?P<state>on)\s+pid:\s+(?P<pid>[\d]+).*uptime:\s+(?P<uptime>[\d\-:]+)')
    response = []
    for line in lines:
        data = parser.search(line).groupdict()
        response.append({
            'id': data['id'],
            'state': data['state'],
            'pid': int(data['pid']),
            'uptime': data['uptime'],
        })
        return response


def status_is_off(lines):
    parser = re.compile(r'[\t]*(?P<id>[^\s]+)[\s]*(?P<state>[^\s]+)[\s]*(?P<help>[^\n\t]+)')
    response = []
    for line in lines:
        data = parser.search(line).groupdict()
        response.append({
            'id': data['id'],
            'state': data['state'],
            'help': data['help'],
        })

    return response


def start(lines, id):
    response = {'id': id}

    if 'ForwardPort array' in lines[0]:
        response['status'] = 'no channels'
    else:
        state = detect_start_state(lines[2])
        if state == 'done':
            response['status'] = 'started'
        elif state == 'failed':
            response['status'] = 'stopped'

        response['pid'] = start_get_site_pid(lines[2])

    return response


def detect_start_state(line):
    parser = re.compile(r'\s*(?P<state>done(?=\s+pid)|failed(?=\s+empty))')

    data = parser.search(line).groupdict()
    state = data['state']
    return state


def start_get_site_pid(line):
    parser = re.compile(r'(?P<pid>\d+$)')

    data = parser.search(line).groupdict()
    pid = int(data['pid'])

    return pid


def stop(lines, id):
    response = {'id': id}

    state = detect_stop_state(lines[1])
    if state == 'done' or state == 'skipped':
        response['status'] = 'stopped'
    elif state == 'failed':
        response['status'] = 'stopped'

    response['pid'] = stop_get_site_pid(lines[1])

    return response


def stop_get_site_pid(line):
    return start_get_site_pid(line)


def detect_stop_state(line):
    parser = re.compile(r'\s*(?P<state>skipped(?=\s+already)|done(?=\s+pid)|failed(?=\s+empty))')

    data = parser.search(line).groupdict()
    state = data['state']
    return state


def restart(lines, id):
    response = {'id': id}

    state = detect_start_state(lines[-1])
    if state == 'done':
        response['status'] = 'restarted'

    response['pid'] = start_get_site_pid(lines[-1])

    return response


def forward_rule(line):
    fields = line.split()
    rule = fields[1].split(':')
    description = line.split('#')[1].strip()
    forward = 'remote' if fields[0] == 'L' else 'local'

    return {
        'id': int(fields[2]) if fields[2] != '#' else -1,
        'ports': {
            'forward': forward,
            'listen': int(rule[1]),
            'send': int(rule[3]),
        },
        'hostname': rule[2],
        'description': description
    }


def list_printers(lines, site):
    response = {
        'id': site,
        'channels': list_channels(lines, site)
    }
    return response


def list_all_printers(lines):
    response = []

    for line in lines:
        if not is_forward_rule(line):
            line = list_sites([line])[0]
            site = line['id']
            hostname = line['hostname']
            response.append({'id': site, 'hostname': hostname, 'channels': []})
        else:
            index = find_site(response, site)
            response[index]['channels'].append(forward_rule(line))

    return response


def list_channels(lines, printer):
    channels = []
    for line in lines:
        if line:
            channels.append(forward_rule(line))

    return channels


def find_site(response, id):
    for i, host in enumerate(response):
        if host['id'] == id:
            return i


def is_forward_rule(line):
    parser = re.compile(r'^(L|R) \*')

    return bool(parser.search(line))


def add_printer(lines):
    response = {}

    for line in lines:
        if is_forward_rule(line):
            response = forward_rule(line)

    return response
