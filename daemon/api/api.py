from flask import Flask
from flask_restful import reqparse, Resource, Api

from api import mast

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()



class Root(Resource):
    def get(self):
        return {
            'output': 'nothing here'
        }


class AddHost(Resource):
    def post(self, name):
        args = parser.parse_args()
        response = mast.Service.add_host(args['name'], args['remote-host'])

        return {
                   name: response['name'],
                   'remote-host': response['remote-host']
               }, 201


class ListHosts(Resource):
    def get(self):
        return {
            'output': mast.list_hosts()
        }


api.add_resource(Root, '/')
api.add_resource(ListHosts, '/list-hosts/')
api.add_resource(AddHost, '/add-host/')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
