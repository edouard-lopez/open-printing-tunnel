import jinja2
import logging

logger = logging.getLogger(__name__)


def render(filename, data):
    package_name = 'scripts'
    env = jinja2.Environment(loader=jinja2.PackageLoader(package_name, 'templates'))

    template = env.get_template(filename)

    return template.render(data)


def prepare_data(optbox, printers, site_host):
    data = []

    for printer in printers:
        data.append({
            'port': printer.get('listening_port'),
            'vps': site_host,
            'imp': printer.get('hostname'),
            'name': optbox
        })

    return data
