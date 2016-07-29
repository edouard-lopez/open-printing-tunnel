import re
import subprocess


def execute(command):
    try:
        response = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8').splitlines()
        return {
            'success': True,
            'output': response
        }
    except subprocess.CalledProcessError as e:
        response = e.output.decode('utf-8').splitlines()
        return {
            'success': False,
            'output': response
        }


def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)