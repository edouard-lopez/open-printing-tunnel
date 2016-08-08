import logging

from flask import Flask
from flask import request
from flask_restful import Resource, Api, abort
from slugify import slugify

from daemon.api import mast_utils
from daemon.api import validators
from daemon.api import daemon

app = Flask(__name__)
api = Api(app)

logger = logging.getLogger(__name__)


class Root(Resource):
    def get(self):
        return {
            'output': 'nothing here'
        }


class Optboxes(Resource):
    def get(self):
        response = mast_utils.list_optboxes()
        return {
                   'success': response['success'],
                   'output': response['output'],
               }, 200 if response['success'] else 500

    def post(self):
        logger.debug(request.json)
        if not request.json or not validators.has_all(request.json, ['name', 'hostname']):
            abort(400)

        optbox_id = slugify(request.json['name'])
        hostname = request.json['hostname']
        if validators.is_valid_host(hostname):
            response = mast_utils.add_optbox(optbox_id, hostname)
            return {
                       'success': response['success'],
                       'output': response['output'],
                       'id': optbox_id,
                       'hostname': hostname,
                   }, 201 if response['success'] else 500


class Optbox(Resource):
    def put(self, optbox_id):
        if not request.json or not validators.has_all(request.json, ['action']):
            abort(400)

        optbox_id = slugify(optbox_id)
        action = slugify(request.json['action'])
        if action not in ['start', 'stop', 'status', 'restart']:
            abort(400)
        response = getattr(daemon, action)(optbox_id)
        return {
                   'success': response['success'],
                   'id': optbox_id,
                   'output': response['output'],
               }, 200 if response['success'] else 500

    def delete(self, optbox_id):
        if not optbox_id:
            abort(400)

        optbox_id = slugify(optbox_id)
        response = mast_utils.remove_optbox(optbox_id)
        return {
                   'success': response['success'],
                   'id': optbox_id,
                   'output': response['output'],
               }, 200 if response['success'] else 500


class Printers(Resource):
    def get(self):
        optbox = '__all__'
        response = mast_utils.list_printers()

        return {
                   'success': response['success'],
                   'optbox': optbox,
                   'output': response['output'],
               }, 200 if response['success'] else 500

    def post(self):
        if not request.json or not validators.has_all(request.json, ['optbox', 'hostname', 'description']):
            abort(400)

        optbox = slugify(request.json['optbox'])
        hostname = request.json['hostname']
        description = request.json['description']
        if validators.is_valid_host(hostname):
            response = mast_utils.add_printer(optbox, hostname)
            return {
                       'optbox': optbox,
                       'output': response['output'],
                       'success': response['success'],
                   }, 201 if response['success'] else 500


class PrintersGet(Resource):
    def get(self, optbox_id=None):
        if optbox_id is None:
            abort(400)
        optbox_id = slugify(optbox_id)
        response = mast_utils.list_printers(optbox_id)

        return {
                   'success': response['success'],
                   'optbox': optbox_id,
                   'output': response['output'],
               }, 200 if response['success'] else 500


class Printer(Resource):
    def delete(self, optbox_id=None, printer_id=None):
        app.logger.debug(optbox_id, printer_id)
        if optbox_id is None or printer_id is None:  # printer_id can have value of 0
            abort(400)

        optbox_id = slugify(optbox_id)
        response = mast_utils.remove_printer(optbox_id, printer_id)
        return {
                   'success': response['success'],
                   'optbox': optbox_id,
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


api.add_resource(Root, '/')
# todo: api.add_resource(AddBulkPrinters, '/optboxes/add-bulk-channels/')
# todo: api.add_resource(CopyLogs, '/optboxes/copy-logs/')
# todo: api.add_resource(Link, '/optboxes/link/')
api.add_resource(Optboxes, '/optboxes/')
api.add_resource(Optbox, '/optboxes/<string:optbox_id>')
api.add_resource(Printers, '/printers/')
api.add_resource(PrintersGet, '/optboxes/<string:optbox_id>/printers/')
api.add_resource(Printer, '/optboxes/<string:optbox_id>/printers/<int:printer_id>')
api.add_resource(Logs, '/logs/')

if __name__ == "__main__":
    app.run()
