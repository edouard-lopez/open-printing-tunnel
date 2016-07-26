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
