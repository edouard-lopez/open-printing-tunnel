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