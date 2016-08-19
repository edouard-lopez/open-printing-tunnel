import logging
import socket
import threading
from timeit import default_timer as timer

import output_parser
import shell

logger = logging.getLogger(__name__)


def ping(hostname):
    command = ['ping', '-q', hostname,
               '-w', '1',
               '-W', '1',
               '-i', '0.2'
               ]

    response = shell.execute(command)

    return output_parser.ping(response['results'])


def telnet(hostname=None, port=22, timeout=0.5, **kwargs):
    start = timer()
    connection = socket.socket()
    connection.settimeout(timeout)
    try:
        connection.connect((hostname, port))
        end = timer()
        delta = end - start
    except (socket.timeout, socket.gaierror) as error:
        logger.debug('telnet error: ', error)
        delta = None
    finally:
        connection.close()

    return {'telnet': delta}


def collect(func, response, **kwargs):
    hostname = kwargs['hostname']

    response[hostname] = func(**kwargs)


def parellelize_telnet(site_id, printers, **kwargs):
    response = {}
    kw = kwargs.copy()
    kw.update({'hostname': site_id})
    collect(telnet, response, **kw)

    printers_response = {}
    threads = []
    for printer in printers:
        hostname = printer['hostname']
        kw = kwargs.copy()
        kw.update({'hostname': hostname})

        threads.append(
            threading.Thread(
                target=collect,
                args=(telnet, printers_response),
                kwargs=kw
            )
        )

    for thread in threads:
        thread.start()
        thread.join()

    response[site_id].update(printers_response)

    return response
