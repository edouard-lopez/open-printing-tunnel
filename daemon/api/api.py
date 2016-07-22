import subprocess
from flask import Flask
from flask_restful import reqparse, Resource, Api

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()


class Root(Resource):
    def get(self):
        return {
            'output': str(subprocess.check_output(["ls"]))
        }

api.add_resource(Root, '/')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
