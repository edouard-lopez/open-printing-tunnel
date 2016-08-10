import logging

from flask import Flask
from flask import Response
from flask import request
from flask_restful import Resource, Api, abort
from slugify import slugify

import scripts
import daemon
import mast_utils
import validators

app = Flask(__name__)
api = Api(app, prefix='/api')

logger = logging.getLogger(__name__)


class Root(Resource):
    def get(self):
        return {
            'results': None
        }


class Sites(Resource):
    def get(self):
        response = mast_utils.list_sites()

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
        response = getattr(daemon, action)(site_id)
        response.update({
            'id': site_id
        })

        return response, 200 if response['cmd']['exit_status'] else 500

    def delete(self, site_id):
        if not site_id:
            abort(400)

        site_id = slugify(site_id)
        response = mast_utils.remove_site(site_id)
        response = response.update({
            'id': site_id,
        })

        return response, 200 if response['cmd']['exit_status'] else 500


class Printers(Resource):
    def get(self):
        site = '__all__'
        response = mast_utils.list_printers()
        response.update({
            'site': site,
        })

        return response, 200 if response['cmd']['exit_status'] else 500

    def post(self):
        if not request.json or not validators.has_all(request.json, ['site', 'hostname', 'description']):
            abort(400)

        site = slugify(request.json['site'])
        hostname = request.json['hostname']
        description = request.json['description']
        if validators.is_valid_host(hostname):
            response = mast_utils.add_printer(site, hostname)
            response = response.update({
                'site': site,
                'hostname': hostname,
                'description': description,
            })

            return response, 201 if response['cmd']['exit_status'] else 500


class PrintersGet(Resource):
    def get(self, site_id=None):
        if site_id is None:
            abort(400)

        site_id = slugify(site_id)
        response = mast_utils.list_printers(site_id)
        response.update({
            'site': site_id,
        })

        return response, 200 if response['cmd']['exit_status'] else 500


class Printer(Resource):
    def delete(self, site_id=None, printer_id=None):
        app.logger.debug(site_id, printer_id)
        if site_id is None or printer_id is None:  # printer_id can have value of 0
            abort(400)

        site_id = slugify(site_id)
        response = mast_utils.remove_printer(site_id, printer_id)
        response = response.update({
            'site': site_id,
            'id': printer_id,
        })

        return response, 200 if response['cmd']['exit_status'] else 500


class Logs(Resource):
    def get(self):
        response = mast_utils.list_logs()

        return response, 200 if response['cmd']['exit_status'] else 500


class PrinterInstallScript(Resource):
    # todo: change to post
    def get(self, site_id, printer_id):
        if not site_id or not printer_id:
            abort(400)

        filename = 'printer.bat.j2'
        site_host = request.headers['Host']

        printers = mast_utils.list_printers(site_id)['results']['channels']
        printer = mast_utils.get_printer(printers, printer_id)
        data = scripts.prepare_printer_install_data(site_id, printer, site_host)
        script = scripts.render(filename, data)

        return Response(script,
                        mimetype='application/bat',
                        headers={"Content-Disposition": "attachment; filename={}-port-{}-{}.bat"
                        .format(site_id, printer['listening_port'], printer['description'])}
                        )


class SiteInstallScript(Resource):
    # todo: change to post
    def get(self, site_id):
        if not site_id:
            abort(400)

        filename = 'site.bat.j2'
        site_host = request.headers['Host']

        printers = mast_utils.list_printers(site_id)['results']['channels']
        data = scripts.prepare_site_install_data(site_id, printers, site_host)
        script = scripts.render(filename, {'sites': data})

        return Response(script,
                        mimetype='application/bat',
                        headers={"Content-Disposition": "attachment; filename={}.bat".format(site_id)})


api.add_resource(Root, '/')
# todo: api.add_resource(AddBulkPrinters, '/sites/add-bulk-channels/')
# todo: api.add_resource(CopyLogs, '/sites/copy-logs/')
# todo: api.add_resource(Link, '/sites/link/')
api.add_resource(Sites, '/sites/')
api.add_resource(Site, '/sites/<string:site_id>')
api.add_resource(Printers, '/printers/')
api.add_resource(PrintersGet, '/sites/<string:site_id>/printers/')
api.add_resource(Printer, '/sites/<string:site_id>/printers/<int:printer_id>')
api.add_resource(Logs, '/logs/')
api.add_resource(PrinterInstallScript, '/scripts/<string:site_id>/printers/<int:printer_id>')
api.add_resource(SiteInstallScript, '/scripts/<string:site_id>')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
