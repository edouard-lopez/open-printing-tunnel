import re
import subprocess


def execute(command):
    try:
        stdout = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8').splitlines()
        return {
            'success': True,
            'output': clean_response(stdout)
        }
    except subprocess.CalledProcessError as e:
        stdout = e.output.decode('utf-8').splitlines()
        return {
            'success': False,
            'output': clean_response(stdout)
        }


def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)


def clean_response(lines):
    cleaned_response = []
    for line in lines:
        if line:
            cleaned_response.append(escape_ansi(line))
    return cleaned_response


