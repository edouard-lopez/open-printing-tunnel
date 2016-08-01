import logging
import re

logger = logging.getLogger(__name__)


def list_hosts(lines):
    parser = re.compile(r'[\t]*(?P<name>[^\s]+)[\s]*(?P<hostname>[^\n\t]+)')
    response = []
    for line in lines:
        data = parser.search(line)
        response.append({
            'name': data.group(1),
            'hostname': data.group(2),
        })

    return response


def status(lines):
    response = []
    for line in lines:
        status = detect_status_state(line)
        if status == 'on':
            return status_is_on(lines)
        elif status == 'off':
            return status_is_off(lines)


def detect_status_state(line):
    parser = re.compile(r'\s*(?P<state>on(?=\s+pid)|off(?=\s+))')

    state = parser.search(line).group(1)
    return state


def status_is_on(lines):
    parser = re.compile(
        r'\s*(?P<name>\w+):autossh\s+(?P<state>on)\s+pid:\s+(?P<pid>[\d]+).*uptime:\s+(?P<uptime>[\d\-:]+)')
    response = []
    for line in lines:
        data = parser.search(line)
        response.append({
            'name': data.group(1),
            'state': data.group(2),
            'pid': int(data.group(3)),
            'uptime': data.group(4),
        })
        return response


def status_is_off(lines):
    parser = re.compile(r'[\t]*(?P<name>[^\s]+)[\s]*(?P<status>[^\s]+)[\s]*(?P<help>[^\n\t]+)')
    response = []
    for line in lines:
        data = parser.search(line)
        response.append({
            'name': data.group(1),
            'state': data.group(2),
            'help': data.group(3),
        })

    return response


def start(lines):
    response = {'name': get_start_optbox_name(lines[0])}

    state = detect_start_state(lines[2])
    if state == 'done':
        response['status'] = 'started'
    elif state == 'failed':
        response['status'] = 'stopped'

    response['pid'] = start_get_optbox_pid(lines[2])

    return response


def detect_start_state(line):
    parser = re.compile(r'\s*(?P<state>done(?=\s+pid)|failed(?=\s+empty))')

    state = parser.search(line).group(1)
    return state


def get_start_optbox_name(line):
    parser = re.compile(r'\s(?P<name>[\w-]+$)')

    name = parser.search(line).group(1)

    return name


def start_get_optbox_pid(line):
    parser = re.compile(r'(?P<pid>\d+$)')

    pid = parser.search(line).group(1)

    return int(pid)


def stop(lines):
    response = {'name': get_stop_optbox_name(lines[0])}

    state = detect_stop_state(lines[1])
    if state == 'done' or state == 'skipped':
        response['status'] = 'stopped'
    elif state == 'failed':
        response['status'] = 'stopped'

    response['pid'] = stop_get_optbox_pid(lines[1])

    return response


def get_stop_optbox_name(line):
    return get_start_optbox_name(line)


def stop_get_optbox_pid(line):
    return start_get_optbox_pid(line)


def detect_stop_state(line):
    parser = re.compile(r'\s*(?P<state>skipped(?=\s+already)|done(?=\s+pid)|failed(?=\s+empty))')

    state = parser.search(line).group(1)
    return state


def restart(lines):
    response = {'name': get_start_optbox_name(lines[0])}

    state = detect_start_state(lines[-1])
    if state == 'done':
        response['status'] = 'restarted'

    response['pid'] = start_get_optbox_pid(lines[-1])

    return response


def forward_rule(line):
    fields = line.split()
    rule = fields[1].split(':')
    description = line.split('#')[1].strip()
    forward = 'normal' if fields[0] == 'L' else 'reverse'

    return {
        'id': int(fields[2]),
        'forward': forward,
        'port': int(rule[1]),
        'hostname': rule[2],
        'description': description
    }


def list_channels(lines):
    response = []
    optbox = None

    for line in lines:
        if is_forward_rule(line):
            optbox = line
            response.append({'name': line, 'channels': []})
        else:
            channels = next((host for host in response if host['name'] == optbox), None)
            response['channels'].append(forward_rule(line))


def is_forward_rule(line):
    parser = re.compile(r'^(L|R) \*')

    return bool(parser.search(line))
