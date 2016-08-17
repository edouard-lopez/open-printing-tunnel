import logging

import output_parser
import shell

logger = logging.getLogger(__name__)

def ping(hostname):
    command = ['ping', '-c', '1', '-W', '1', '-q', hostname]

    response = shell.execute(command)
    return output_parser.ping(response['results'])
