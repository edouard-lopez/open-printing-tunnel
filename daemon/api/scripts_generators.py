import jinja2
import logging

logger = logging.getLogger(__name__)


def render(filename, data):
    package_name = 'scripts_generators'
    env = jinja2.Environment(loader=jinja2.PackageLoader(package_name, 'templates'))

    template = env.get_template(filename)

    return template.render(data)


def prepare_site_install_data(site_id, printers, site_host):
    data = []

    for printer in printers:
        data.append(prepare_printer_install_data(site_id, printer, site_host))

    return data


def prepare_printer_install_data(site_id, printer, site_host):
    return {
        'port': printer['ports']['listen'],
        'vps': site_host,
        'imp': printer.get('hostname'),
        'name': site_id
    }
