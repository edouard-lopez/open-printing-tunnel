import logging
import socket
import threading
from timeit import default_timer as timer

import output_parser
import shell

logger = logging.getLogger(__name__)


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


def telnet(hostname=None, port=22, timeout=0.5, **kwargs):
    logger.debug('hostname', hostname)
    start = timer()
    connection = socket.socket()
    connection.settimeout(timeout)
    try:
        connection.connect((hostname, port))
        end = timer()
        delta = end - start
    except:
        delta = None
    finally:
        connection.close()

    return {'telnet': delta}


def collect(task, response, **kwargs):
    hostname = kwargs['hostname']

    response[hostname] = task(**kwargs)


def parellelize(task, site_id, printers, **kwargs):
    response = {}
    kw = kwargs.copy()
    kw.update({'hostname': site_id})
    collect(task, response, **kw)

    printers_response = {}
    threads = []
    for printer in printers:
        hostname = printer['hostname']
        kw = kwargs.copy()
        kw.update({'hostname': hostname})

        threads.append(
            threading.Thread(
                target=collect,
                args=(task, printers_response),
                kwargs=kw
            )
        )

    for thread in threads:
        thread.start()
        thread.join()

    response[site_id].update(printers_response)

    return response


def ping_site_and_printers(site_hostname, printers):
    hostnames = [site_hostname]
    printers_hostnames = [printer['hostname'] for printer in printers]

    response = fping([site_hostname])
    if len(printers_hostnames) > 0:
        response[site_hostname].update(fping(printers_hostnames))

    return response


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