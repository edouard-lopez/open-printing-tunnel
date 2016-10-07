import logging
import re

logger = logging.getLogger(__name__)


def list_sites(lines):
    parser = re.compile(r'[\s]*(?P<id>[^\s]+)[\s]*(?P<hostname>[^\n\t]+)')
    response = []
    for line in lines:
        matches = parser.search(line)
        if matches:
            data = matches.groupdict()
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
    matches = parser.search(line)

    if matches:
        data = matches.groupdict()
        state = data['state']
    else:
        logger.debug(line)
        state = 'unknown'

    return state


def status_is_on(lines):
    parser = re.compile(
        r'\s*(?P<id>\w+):autossh\s+(?P<state>on)\s+pid:\s+(?P<pid>[\d]+).*uptime:\s+(?P<uptime>[\d\-:]+)')
    response = []
    for line in lines:
        matches = parser.search(line)
        if matches:
            data = matches.groupdict()
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
        matches = parser.search(line)
        if matches:
            data = matches.groupdict()
            response.append({
                'id': data['id'],
                'state': data['state'],
                'help': data['help'],
            })

    return response


def start(lines, id):
    response = {'id': id}

    if 'ForwardPort array' in lines[0]:
        response['status'] = 'empty'
        response['help'] = 'no channels'
    else:
        state = detect_start_state(lines[2])

        response['status'] = 'started' if state == 'done' else 'stopped'
        response['pid'] = start_get_site_pid(lines[2])

    return response


def detect_start_state(line):
    state = None
    parser = re.compile(r'\s*(?P<state>done(?=\s+pid)|failed(?=\s+empty))')
    matches = parser.search(line)

    if matches:
        data = matches.groupdict()
        state = data['state']

    return state


def start_get_site_pid(line):
    pid = None
    parser = re.compile(r'(?P<pid>\d+$)')
    matches = parser.search(line)

    if matches:
        data = matches.groupdict()
        if data['pid']:
            pid = int(data['pid'])

    return pid


def stop(lines, id):
    response = {'id': id}

    state = detect_stop_state(lines[1])
    response['status'] = 'stopped' if state == 'done' else state
    response['pid'] = stop_get_site_pid(lines[1])

    return response


def stop_get_site_pid(line):
    return start_get_site_pid(line)


def detect_stop_state(line):
    state = None
    parser = re.compile(r'\s*(?P<state>skipped(?=\s+already)|done(?=\s+pid)|failed(?=\s+empty))')
    matches = parser.search(line)

    if matches:
        data = matches.groupdict()
        state = data['state']

    return state


def restart(lines, id):
    response = {'id': id}

    last_line = lines[-1]
    restarting_line = lines[1]
    state = detect_stop_state(restarting_line)

    response['status'] = 'restarted' if state == 'done' else state
    response['pid'] = start_get_site_pid(last_line)

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
    sites = {}
    site_id = None
    for line in lines:
        if is_forward_rule(line):
            sites[site_id]['channels'].append(forward_rule(line))
        else:
            site_info = list_sites([line])[0]
            site_id = site_info['id']
            sites[site_id] = {
                'id': site_id,
                'hostname': site_info['hostname'],
                'channels': []
            }
    return list(sites.values())


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


def fping(stdout):
    response = {}

    for line in stdout:
        if 'alive' in line:
            parser = re.compile(r'(?P<hostname>[^\s]+).+\((?P<time>[\d.]+)\s')
            matches = parser.search(line)
            data = matches.groupdict()

            response[data['hostname']] = {'ping': float(data['time'])}
        else:
            hostname = line.split()[0]
            response[hostname] = {'ping': None}

    return response
