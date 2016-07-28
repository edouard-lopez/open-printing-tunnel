from flask import Flask
from flask import request
from flask_restful import Resource, Api, abort
from slugify import slugify

import mast_utils
import validators

app = Flask(__name__)
api = Api(app)


class Root(Resource):
    def get(self):
        return {
            'output': 'nothing here'
        }


class AddHost(Resource):
    def post(self):
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


class ListHosts(Resource):
    def get(self):
        response = mast_utils.list_hosts()
        return {
                   'success': response['success'],
                   'output': response['output'],
               }, 201 if response['success'] else 500


class RemoveHost(Resource):
    def post(self):
        if not request.json or not validators.has_all(request.json, ['name']):
            abort(400)

        name = slugify(request.json['name'])
        response = mast_utils.remove_channel(name)
        return {
                   'success': response['success'],
                   'name': name,
                   'output': response['output'],
               }, 201 if response['success'] else 500


class AddChannel(Resource):
    def post(self):
        if not request.json or not validators.has_all(request.json, ['name', 'hostname', 'description']):
            abort(400)

        name = slugify(request.json['name'])
        hostname = request.json['hostname']
        description = request.json['description']
        if validators.is_valid_host(hostname):
            response = mast_utils.add_channel(name, hostname)
            return {
                       'success': response['success'],
                       'name': name,
                       'description': description,
                       'hostname': hostname,
                       'output': response['output'],
                   }, 201 if response['success'] else 500


class ListChannels(Resource):
    def get(self):
        if request.json:
            if not validators.has_all(request.json, ['name']):
                abort(400)
            else:
                name = slugify(request.json['name'])
                response = mast_utils.list_channels(name)
        else:
            response = mast_utils.list_channels()
            name = '*'

        return {
                   'success': response['success'],
                   'name': name,
                   'output': response['output'],
               }, 201 if response['success'] else 500


class RemoveChannel(Resource):
    def post(self):
        if not request.json or not validators.has_all(request.json, ['id', 'name']):
            abort(400)

        name = slugify(request.json['name'])
        response = mast_utils.remove_channel(id, name)
        return {
                   'success': response['success'],
                   'id': id,
                   'name': name,
                   'output': response['output'],
               }, 201 if response['success'] else 500


class ListLogs(Resource):
    def get(self):
        response = mast_utils.list_logs()
        return {
                   'success': response['success'],
                   'output': response['output'],
               }, 201 if response['success'] else 500


class Restart(Resource):
    def put(self):
        if not request.json or not validators.has_all(request.json, ['name']):
            abort(400)

        name = slugify(request.json['name'])
        response = mast_utils.restart(name)
        return {
                   'success': response['success'],
                   'name': name,
                   'output': response['output'],
               }, 201 if response['success'] else 500


class Start(Resource):
    def put(self):
        if not request.json or not validators.has_all(request.json, ['name']):
            abort(400)

        name = slugify(request.json['name'])
        response = mast_utils.start(name)
        return {
                   'success': response['success'],
                   'name': name,
                   'output': response['output'],
               }, 201 if response['success'] else 500


class Status(Resource):
    def put(self):
        if not request.json or not validators.has_all(request.json, ['name']):
            abort(400)

        name = slugify(request.json['name'])
        response = mast_utils.status(name)
        return {
                   'success': response['success'],
                   'name': name,
                   'output': response['output'],
               }, 201 if response['success'] else 500


class Stop(Resource):
    def put(self):
        if not request.json or not validators.has_all(request.json, ['name']):
            abort(400)

        name = slugify(request.json['name'])
        response = mast_utils.stop(name)
        return {
                   'success': response['success'],
                   'name': name,
                   'output': response['output'],
               }, 201 if response['success'] else 500


api.add_resource(Root, '/')
# api.add_resource(AddBulkChannels, '/add-bulk-channels/')
api.add_resource(AddChannel, '/add-channel/')
api.add_resource(AddHost, '/add-host/')
# api.add_resource(CopyLogs, '/copy-logs/')
# api.add_resource(Link, '/link/')
api.add_resource(ListChannels, '/list-channels/')
api.add_resource(ListHosts, '/list-hosts/')
api.add_resource(ListLogs, '/list-logs/')
api.add_resource(RemoveChannel, '/remove-channel/')
api.add_resource(RemoveHost, '/remove-host/')
api.add_resource(Restart, '/restart/')
api.add_resource(Start, '/start/')
api.add_resource(Status, '/status/')
api.add_resource(Stop, '/stop/')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
