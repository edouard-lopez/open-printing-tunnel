import logging
import socket
from timeit import default_timer as timer

import output_parser
import shell

logger = logging.getLogger(__name__)


def ping(hostname):
    command = ['ping', '-c', '1', '-W', '1', '-q', hostname]

    response = shell.execute(command)
    return output_parser.ping(response['results'])


def telnet(hostname, port=23, timeout=1):
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

    return {
        hostname: delta
    }
