import re


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
        status = detect_status(line)
        if status == 'on':
            return status_is_on(lines)
        elif status == 'off':
            return status_is_off(lines)


def detect_status(line):
    parser = re.compile(r'\s*(?P<state>on(?=\s+pid)|off(?=\s+))')

    state = parser.search(line).group(1)
    return state


def status_is_on(lines):
    parser = re.compile(
        r'\s*(?P<name>\w+):autossh\s+(?P<state>on)\s+pid:\s+(?P<pid>[\d]+).*uptime:\s+(?P<uptime>\d+:\d+:\d+)')
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
