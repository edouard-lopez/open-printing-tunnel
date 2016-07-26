import subprocess
from flask import Flask
from flask_restful import reqparse, Resource, Api

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()


class Mast():
    service = '/etc/init.d/mast'
    makefile = '/usr/sbin/mast-utils'


class Root(Resource):
    def get(self):
        return {
            'output': str(subprocess.check_output(["ls"]))
        }


class ListHosts(Resource):
    def get(self):
        cmd = [Mast.makefile, 'list-hosts']
        return str(subprocess.check_output(cmd))


api.add_resource(Root, '/')
api.add_resource(ListHosts, '/list-hosts/')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
