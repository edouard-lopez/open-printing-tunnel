from flask import Flask
from flask import request
from flask_restful import Resource, Api, abort

from api import mast
from api import validators

app = Flask(__name__)
api = Api(app)


class Root(Resource):
    def get(self):
        return {
            'output': 'nothing here'
        }


class AddHost(Resource):
    def post(self):
        if not request.json or not validators.has_all(request.json, ['name', 'remote-host']):
            abort(400)

        response = mast.Daemon.add_host(request.json['name'], request.json['remote-host'])

        return {
                   'name': response['name'],
                   'remote-host': response['remote-host']
               }, 201


class ListHosts(Resource):
    def get(self):
        return mast.Utils.list_hosts()


api.add_resource(Root, '/')
api.add_resource(ListHosts, '/list-hosts/')
api.add_resource(AddHost, '/add-host/')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
