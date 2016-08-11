import re
import subprocess


def execute(command):
    try:
        stdout = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8').splitlines()
        response = {
            'cmd': {
                'command': " ".join(command),
                'raw': stdout,
                'exit_status': True
            }
        }
        response.update({'results': clean_response(stdout)})

        return response
    except subprocess.CalledProcessError as e:
        stdout = e.output.decode('utf-8').splitlines()
        response = {
            'cmd': {
                'raw': stdout,
                'exit_status': False
            }
        }
        response.update({'results': clean_response(stdout)})

        return response


def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)


def clean_response(lines):
    cleaned_response = []
    for line in lines:
        if line:
            cleaned_response.append(escape_ansi(line.strip()))
    return cleaned_response
