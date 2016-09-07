import logging

import jinja2

logger = logging.getLogger(__name__)


def render(filename, data):
    package_name = 'scripts_generators'
    env = jinja2.Environment(loader=jinja2.PackageLoader(package_name, 'templates'))

    template = env.get_template(filename)

    return template.render(data)


def prepare_site_install_data(site_id, printers, site_host, now):
    data = []

    for printer in printers:
        data.append(prepare_printer_install_data(site_id, printer, site_host, now))

    return data


def prepare_printer_install_data(site_id, printer, site_host, now):
    return {
        'port': printer['ports']['listen'],
        'site_hostname': site_host,
        'hostname': printer.get('hostname'),
        'site': site_id,
        'description': printer.get('description'),
        'datetime': now
    }
