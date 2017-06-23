import logging
import sys
from datetime import datetime

from flask import Flask
from flask import Response
from flask import request
from flask_restful import Resource, Api, abort
from slugify import slugify

import daemon
import mast_utils
import network_utils
import scripts_generators
import validators
from network_tools import NetworkTools
from scanner import Scanner

app = Flask(__name__)
api = Api(app, prefix='/api')

logger = logging.getLogger(__name__)


def configure_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)


configure_logging()

if not app.debug:
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.DEBUG)
    logging.getLogger('gunicorn').setLevel(logging.DEBUG)
    logging.getLogger('gunicorn.access').setLevel(logging.DEBUG)
    logging.getLogger('gunicorn.error').setLevel(logging.DEBUG)


class Root(Resource):
    def get(self):
        return {
            'results': None
        }


class Sites(Resource):
    def get(self):
        response = mast_utils.list_site_and_printers()

        return response, 200 if response['cmd']['exit_status'] else 500

    def post(self):
        if not request.json or not validators.has_all(request.json, ['id', 'hostname']):
            abort(400)

        site_id = slugify(request.json['id'])
        hostname = request.json['hostname']
        if validators.is_valid_host(hostname):
            response = mast_utils.add_site(site_id, hostname)
            response.update({
                'id': site_id, 'hostname': hostname
            })

            return response, 201 if response['cmd']['exit_status'] else 500


class Site(Resource):
    def put(self, site_id):
        if not request.json or not validators.has_all(request.json, ['action']):
            abort(400)

        site_id = slugify(site_id)
        action = slugify(request.json['action'])
        if action not in ['start', 'stop', 'status', 'restart']:
            abort(400)
        response = getattr(daemon, action)(site_id)  # see api/daemon.py
        response.update({
            'id': site_id
        })

        return response, 200 if response['cmd']['exit_status'] else 500

    def delete(self, site_id):
        if not site_id:
            abort(400)

        site_id = slugify(site_id)
        response = getattr(daemon, 'stop')(site_id)  # see api/daemon.py
        response = mast_utils.remove_site(site_id)
        response['id'] = site_id

        return response, 200 if response['cmd']['exit_status'] else 500


class Printers(Resource):
    def post(self):
        if not request.json or not validators.has_all(request.json, ['site', 'hostname', 'description']):
            abort(400)

        site = slugify(request.json['site'])
        hostname = request.json['hostname']
        description = request.json['description']
        if validators.is_valid_host(hostname):
            response = mast_utils.add_printer(site, hostname, description)
            response.update({
                'site': site,
                'hostname': hostname,
                'description': description,
            })

            return response, 201 if response['cmd']['exit_status'] else 500


class Printer(Resource):
    def delete(self, site_id=None, printer_id=None):
        if site_id is None or printer_id is None:  # printer_id can have value of 0
            abort(400)

        site_id = slugify(site_id)
        response = mast_utils.remove_printer(site_id, printer_id)
        response.update({
            'site': site_id,
            'id': printer_id,
        })

        return response, 200 if response['cmd']['exit_status'] else 500


class PrinterInstallScript(Resource):
    def get(self, site_id, printer_id):
        filename = 'printer.bat.j2'
        site_host = request.headers['Host']
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        printers = mast_utils.list_printers(site_id)['results']['channels']
        printer = mast_utils.get_printer(printers, printer_id)
        data = scripts_generators.prepare_printer_install_data(site_id, printer, site_host, now)
        script = scripts_generators.render(filename, data)

        return Response(
            script,
            mimetype='application/bat',
            headers={"Content-Disposition": "attachment; filename={}-port-{}-{}.bat".format(
                site_id,
                printer['ports']['listen'],
                printer['description']
            )
            }
        )


class SiteInstallScript(Resource):
    def get(self, site_id):
        if not site_id:
            abort(400)

        filename = 'site.bat.j2'
        site_host = request.headers['Host']
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        printers = mast_utils.list_printers(site_id)['results']['channels']
        data = scripts_generators.prepare_site_install_data(site_id, printers, site_host, now)
        script = scripts_generators.render(filename, {'printers': data})

        return Response(
            script,
            mimetype='application/bat',
            headers={"Content-Disposition": "attachment; filename={}.bat".format(site_id)}
        )

class SiteConfigurePortScript(Resource):
    def get(self, site_id):
        if not site_id:
            abort(400)

        filename = 'configure-ports.bat.j2'
        site_host = request.headers['Host']
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        printers = mast_utils.list_printers(site_id)['results']['channels']
        data = scripts_generators.prepare_site_install_data(site_id, printers, site_host, now)
        script = scripts_generators.render(filename, {'printers': data})

        return Response(
            script,
            mimetype='application/bat',
            headers={"Content-Disposition": "attachment; filename={}-configure-ports.bat".format(site_id)}
        )


class Networks(Resource):
    def get(self):
        response, telnets, pings = {}, {}, {}
        sites = mast_utils.list_sites()['results']

        for site in sites:
            printers = mast_utils.list_printers(site['id'])['results']['channels']
            telnets.update(network_utils.parellelize(network_utils.telnet, site['hostname'], printers))
            pings.update(network_utils.ping_site_and_printers(site['hostname'], printers))

        response = pings.copy()
        network_utils.deep_merge(response, telnets)
        return response


class Scan(Resource):
    def get(self, site_hostname):
        scanner = Scanner(network_tools=NetworkTools(), hostname=site_hostname)
        scan = scanner.scan(port=9100)
        return scan


api.add_resource(Root, '/')
api.add_resource(Sites, '/sites/')
api.add_resource(Site, '/sites/<string:site_id>/')
api.add_resource(Printers, '/printers/')
api.add_resource(Printer, '/sites/<string:site_id>/printers/<int:printer_id>/')
api.add_resource(PrinterInstallScript, '/scripts/<string:site_id>/printers/<int:printer_id>/')
api.add_resource(SiteInstallScript, '/scripts/<string:site_id>/')
api.add_resource(SiteConfigurePortScript, '/scripts/<string:site_id>/ports/')
api.add_resource(Networks, '/networks/')
api.add_resource(Scan, '/scan/<string:site_hostname>/')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
