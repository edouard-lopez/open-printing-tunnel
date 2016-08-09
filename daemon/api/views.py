import logging

from flask import Flask
from flask import Response
from flask import request
from flask_restful import Resource, Api, abort
from slugify import slugify

import scripts
from daemon.api import daemon
from daemon.api import mast_utils
from daemon.api import validators

app = Flask(__name__)
api = Api(app, prefix='/daemon')

logger = logging.getLogger(__name__)


class Root(Resource):
    def get(self):
        return {
            'output': 'nothing here'
        }


class Sites(Resource):
    def get(self):
        response = mast_utils.list_sites()
        return {
                   'success': response['success'],
                   'output': response['output'],
               }, 200 if response['success'] else 500

    def post(self):
        if not request.json or not validators.has_all(request.json, ['name', 'hostname']):
            abort(400)

        site_id = slugify(request.json['name'])
        hostname = request.json['hostname']
        if validators.is_valid_host(hostname):
            response = mast_utils.add_site(site_id, hostname)
            return {
                       'success': response['success'],
                       'output': response['output'],
                       'id': site_id,
                       'hostname': hostname,
                   }, 201 if response['success'] else 500


class Site(Resource):
    def put(self, site_id):
        if not request.json or not validators.has_all(request.json, ['action']):
            abort(400)

        site_id = slugify(site_id)
        action = slugify(request.json['action'])
        if action not in ['start', 'stop', 'status', 'restart']:
            abort(400)
        response = getattr(daemon, action)(site_id)
        return {
                   'success': response['success'],
                   'id': site_id,
                   'output': response['output'],
               }, 200 if response['success'] else 500

    def delete(self, site_id):
        if not site_id:
            abort(400)

        site_id = slugify(site_id)
        response = mast_utils.remove_site(site_id)
        return {
                   'success': response['success'],
                   'id': site_id,
                   'output': response['output'],
               }, 200 if response['success'] else 500


class Printers(Resource):
    def get(self):
        site = '__all__'
        response = mast_utils.list_printers()

        return {
                   'success': response['success'],
                   'site': site,
                   'output': response['output'],
               }, 200 if response['success'] else 500

    def post(self):
        if not request.json or not validators.has_all(request.json, ['site', 'hostname', 'description']):
            abort(400)

        site = slugify(request.json['site'])
        hostname = request.json['hostname']
        description = request.json['description']
        if validators.is_valid_host(hostname):
            response = mast_utils.add_printer(site, hostname)
            return {
                       'site': site,
                       'output': response['output'],
                       'success': response['success'],
                   }, 201 if response['success'] else 500


class PrintersGet(Resource):
    def get(self, site_id=None):
        if site_id is None:
            abort(400)
        site_id = slugify(site_id)
        response = mast_utils.list_printers(site_id)

        return {
                   'success': response['success'],
                   'site': site_id,
                   'output': response['output'],
               }, 200 if response['success'] else 500


class Printer(Resource):
    def delete(self, site_id=None, printer_id=None):
        app.logger.debug(site_id, printer_id)
        if site_id is None or printer_id is None:  # printer_id can have value of 0
            abort(400)

        site_id = slugify(site_id)
        response = mast_utils.remove_printer(site_id, printer_id)
        return {
                   'success': response['success'],
                   'site': site_id,
                   'id': printer_id,
                   'output': response['output'],
               }, 200 if response['success'] else 500


class Logs(Resource):
    def get(self):
        response = mast_utils.list_logs()
        return {
                   'success': response['success'],
                   'output': response['output'],
               }, 200 if response['success'] else 500


class PrinterInstallScript(Resource):
    # todo: change to post
    def get(self, site_id, printer_id):
        if not site_id or not printer_id:
            abort(400)

        filename = 'printer.bat.j2'
        site_host = request.headers['Host']

        printers = mast_utils.list_printers(site_id)['output']['channels']
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

        printers = mast_utils.list_printers(site_id)['output']['channels']
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
    app.run()
