import logging

from flask import Flask
from flask import request
from flask_restful import Resource, Api, abort
from slugify import slugify

import daemon
import mast_utils
import validators

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
        response = mast_utils.list_hosts()
        return {
                   'success': response['success'],
                   'output': response['output'],
               }, 200 if response['success'] else 500

    def post(self):
        logger.debug(request.json)
        if not request.json or not validators.has_all(request.json, ['name', 'hostname']):
            abort(400)

        name = slugify(request.json['name'])
        hostname = request.json['hostname']
        if validators.is_valid_host(hostname):
            response = mast_utils.add_host(name, hostname)
            return {
                       'success': response['success'],
                       'output': response['output'],
                       'name': name,
                       'hostname': hostname,
                   }, 201 if response['success'] else 500

    def delete(self):
        if not request.json or not validators.has_all(request.json, ['id', 'name']):
            abort(400)

        name = slugify(request.json['name'])
        response = mast_utils.remove_host(name)
        return {
                   'success': response['success'],
                   'id': id,
                   'name': name,
                   'output': response['output'],
               }, 200 if response['success'] else 500


class Printers(Resource):
    def get(self):
        if request.json:
            if not validators.has_all(request.json, ['optbox']):
                abort(400)
            else:
                optbox = slugify(request.json['optbox'])
                response = mast_utils.list_channels(optbox)
        else:
            response = mast_utils.list_channels()
            optbox = '*'

        return {
                   'success': response['success'],
                   'optbox': optbox,
                   'output': response['output'],
               }, 200 if response['success'] else 500

    def delete(self):
        if not request.json or not validators.has_all(request.json, ['name']):
            abort(400)

        name = slugify(request.json['name'])
        response = mast_utils.remove_channel(name)
        return {
                   'success': response['success'],
                   'name': name,
                   'output': response['output'],
               }, 200 if response['success'] else 500

    def post(self):
        if not request.json or not validators.has_all(request.json, ['optbox', 'hostname', 'description']):
            abort(400)

        optbox = slugify(request.json['optbox'])
        hostname = request.json['hostname']
        description = request.json['description']
        if validators.is_valid_host(hostname):
            response = mast_utils.add_channel(optbox, hostname)
            return {
                       'success': response['success'],
                       'optbox': optbox,
                       'description': description,
                       'hostname': hostname,
                       'output': response['output'],
                   }, 201 if response['success'] else 500

    def put(self):
        if not request.json or not validators.has_all(request.json, ['optbox', 'action']):
            abort(400)

        optbox = slugify(request.json['optbox'])
        action = slugify(request.json['action'])
        if action not in ['start', 'stop', 'status', 'restart']:
            abort(400)
        response = getattr(daemon, action)(optbox)
        return {
                   'success': response['success'],
                   'optbox': optbox,
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
api.add_resource(Printers, '/printers/')
api.add_resource(Optboxes, '/optboxes/')
api.add_resource(Logs, '/logs/')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
