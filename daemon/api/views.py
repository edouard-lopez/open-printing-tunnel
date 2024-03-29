import os
from datetime import datetime

from flask import Flask, Response, request
from flask_restful import Api, Resource, abort
from slugify import slugify

import daemon
import http_status
import mast_utils
import network_utils
import scripts_generators
import validators
from config_constraints import Constraints
from config_editor import ConfigEditor
from network_tools import NetworkTools
from scanner import Scanner

app = Flask(__name__)
api = Api(app, prefix='/api')


class Root(Resource):
    def get(self):
        return {
            'results': None
        }


class Sites(Resource):
    def get(self):
        response = mast_utils.list_site_and_printers()

        return response, http_status.OK if response['cmd']['exit_status'] else http_status.INTERNAL_SERVER_ERROR

    def post(self):
        if not request.json or not validators.has_all(request.json, ['id', 'hostname']):
            abort(http_status.BAD_REQUEST)

        hostname = request.json['hostname']
        if not validators.is_valid_host(hostname):
            return None, http_status.INTERNAL_SERVER_ERROR

        site_id = slugify(request.json['id'])
        response = mast_utils.add_site(site_id, hostname)
        response.update({
            'id': site_id,
            'hostname': hostname
        })

        return response, http_status.CREATED if response['cmd']['exit_status'] else http_status.INTERNAL_SERVER_ERROR


class Site(Resource):
    def put(self, site_id):
        if not request.json or not validators.has_all(request.json, ['action']):
            abort(http_status.BAD_REQUEST)

        site_id = slugify(site_id)
        action = slugify(request.json['action'])
        if action not in ['start', 'stop', 'status', 'restart']:
            abort(http_status.BAD_REQUEST)
        response = getattr(daemon, action)(site_id)  # see api/daemon.py
        response.update({
            'id': site_id
        })

        return response, http_status.OK if response['cmd']['exit_status'] else http_status.INTERNAL_SERVER_ERROR

    def delete(self, site_id):
        if not site_id:
            abort(http_status.BAD_REQUEST)

        site_id = slugify(site_id)
        response = getattr(daemon, 'stop')(site_id)  # see api/daemon.py
        response = mast_utils.remove_site(site_id)
        response['id'] = site_id

        return response, http_status.OK if response['cmd']['exit_status'] else http_status.INTERNAL_SERVER_ERROR


class Config(Resource):
    def get(self, site_id):
        site_id = slugify(site_id)

        site_config = os.path.join('/etc', 'mast', site_id)
        content = ConfigEditor().load(file_path=site_config)

        only = ['ForwardPort', 'BandwidthLimitation', 'UploadLimit', 'DownloadLimit']
        censored = Constraints().censor(config=content, keep=only)

        return censored, http_status.OK

    def put(self, site_id):
        if not request.json:
            abort(http_status.BAD_REQUEST)
        site_id = slugify(site_id)
        site_config = os.path.join('/etc', 'mast', site_id)
        config_editor = ConfigEditor()

        BANDWIDTH_MIN = 10
        BANDWIDTH_MAX = 100000
        for key in ['UploadLimit', 'DownloadLimit']:
            if key in request.json:
                value = request.json.get(key)
                assert isinstance(int(float(value)), int), "Bandwidth must be a positive integer."
                assert BANDWIDTH_MIN <= value <= BANDWIDTH_MAX, "Bandwidth must be between {}Kb and {}Kb." % (
                    BANDWIDTH_MIN, BANDWIDTH_MAX)
                config_editor.update(file_path=site_config, data={key: value})

        content = config_editor.load(file_path=site_config)
        only = ['ForwardPort', 'BandwidthLimitation', 'UploadLimit', 'DownloadLimit']
        censored = Constraints().censor(config=content, keep=only)

        return censored, http_status.OK


class Printers(Resource):

    def post(self):
        if not request.json:
            abort(http_status.BAD_REQUEST)

        if not validators.has_all(request.json, ['site', 'hostname', 'description']):
            abort(http_status.BAD_REQUEST)

        hostname = request.json['hostname']
        if not validators.is_valid_host(hostname):
            abort(http_status.BAD_REQUEST)

        site_id = slugify(request.json['site'])
        description = request.json['description']

        if 'ports' in request.json and 'listen' in request.json['ports']:
            if not validators.has_all(request.json['ports'], ['forward', 'listen', 'send']):
                abort(http_status.BAD_REQUEST)
            assert isinstance(int(float(request.json['ports']['listen'])), int), "Bandwidth must be a positive integer."

            config_editor = ConfigEditor()
            listening_port = config_editor.cast_to_int(request.json['ports']['listen'])

            PORT_NUMBER_MIN = 1000
            PORT_NUMBER_MAX = 65535
            if not PORT_NUMBER_MIN <= listening_port <= PORT_NUMBER_MAX:
                abort(http_status.NOT_ACCEPTABLE)

            sites = mast_utils.list_site_and_printers()['results']
            if listening_port in config_editor.aggregate_listening_ports(sites):
                abort(http_status.CONFLICT)

            site_config = os.path.join('/etc', 'mast', site_id)
            config = config_editor.load(file_path=site_config)
            ruleset = config_editor.parse_forward_ruleset(config['ForwardPort'])
            new_rule = {'site': site_id, 'hostname': hostname, 'description': description,
                        'ports': request.json['ports']}
            ruleset.append(new_rule)
            config_editor.update(file_path=site_config,
                                 data={'ForwardPort': config_editor.serialize_forward_ruleset(ruleset)})
            config = config_editor.load(file_path=site_config)
            response = {'results': new_rule, 'cmd': {'exit_status': True}}
        else:
            response = mast_utils.add_printer(site_id, hostname, description)
            response.update({
                'site': site_id,
                'hostname': hostname,
                'description': description,
            })

        return response, http_status.CREATED if response['cmd']['exit_status'] else http_status.INTERNAL_SERVER_ERROR


class Printer(Resource):
    def delete(self, site_id=None, printer_id=None):
        if site_id is None or printer_id is None:  # printer_id can have value of 0
            abort(http_status.BAD_REQUEST)

        site_id = slugify(site_id)
        response = mast_utils.remove_printer(site_id, printer_id)
        response.update({
            'site': site_id,
            'id': printer_id,
        })

        return response, http_status.OK if response['cmd']['exit_status'] else http_status.INTERNAL_SERVER_ERROR


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
            abort(http_status.BAD_REQUEST)

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
            abort(http_status.BAD_REQUEST)

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
api.add_resource(Config, '/config/<string:site_id>/')
api.add_resource(Printers, '/printers/')
api.add_resource(Printer, '/sites/<string:site_id>/printers/<int:printer_id>/')
api.add_resource(PrinterInstallScript, '/scripts/<string:site_id>/printers/<int:printer_id>/')
api.add_resource(SiteInstallScript, '/scripts/<string:site_id>/')
api.add_resource(SiteConfigurePortScript, '/scripts/<string:site_id>/ports/')
api.add_resource(Networks, '/networks/')
api.add_resource(Scan, '/scan/<string:site_hostname>/')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
