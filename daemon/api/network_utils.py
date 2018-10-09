import logging
import socket
import threading

import output_parser
import shell

logger = logging.getLogger(__name__)


# fixme: merge into network_tools
def fping(hostnames):
    command = ['fping',
               '-p', '100',
               '-r', '0',
               '-t', '300',
               '-e',
               ]
    command.extend(hostnames)

    response = shell.execute(command)

    return output_parser.fping(response['results'])


# fixme: merge into network_tools
def telnet(hostname=None, port=22, timeout=0.3, **kwargs):
    logger.debug('telnet: {}:{}'.format(hostname, port))

    connection = socket.socket()
    connection.settimeout(timeout)
    try:
        connection.connect((hostname, port))
        reachable = True
    except:
        reachable = False
    finally:
        connection.close()
        del connection

    return {'telnet': reachable}


# fixme: merge into network_tools
def collect(task, response, **kwargs):
    hostname = kwargs['ip']

    response[hostname] = task(**kwargs)


# fixme: merge into network_tools
def parellelize(task, site_id, printers, **kwargs):
    response = {}
    kw = kwargs.copy()
    kw.update({'hostname': site_id})
    response.update({site_id: task(**kw)})

    printers_response = {}
    threads = []
    for printer in printers:
        kw = kwargs.copy()
        kw.update({
            'hostname': 'localhost',
            'ip': (printer['hostname']),
            'port': (printer['ports']['listen'])
        })

        thread = threading.Thread(target=collect, args=(task, printers_response), kwargs=kw)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    response[site_id].update(printers_response)

    return response


# fixme: merge into network_tools
def ping_site_and_printers(site_hostname, printers):
    hostnames = [site_hostname]
    printers_hostnames = [printer['hostname'] for printer in printers]

    response = fping([site_hostname])
    if len(printers_hostnames) > 0:
        response[site_hostname].update(fping(printers_hostnames))

    return response


# fixme: merge into network_tools
def deep_merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                deep_merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a
