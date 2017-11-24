from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse

#  https://flask-restful.readthedocs.io/en/latest/quickstart.html
#  Use Postman desktop application for testing
# MongoDB automatically in JSON

# r = requests.get()
# r_text = r.json()

app = Flask(__name__)
api = Api(app)

class fileListApi(Resource):
    def __init__(self):  # Upon initialisation of the class
        global fileS
        self.server = fileS
        print ('server', self.server.files)
        super(fileListApi, self).__init__()  # Initialising the Resource class
        self.reqparser = reqparse.RequestParser()

        # For every value coming in JSON, you need an argument
        self.reqparser.add_argument('name', type=str, location = 'json')  # Repeat for multiple variables
        # e.g to add a client_ID value do:
        # self.reqparser.add_argument('client_ID', type=str, location = 'json')  # Repeat for multiple variables

    def get(self):
        return {"Files": self.server.files}
        # return {"Hello": "World"}  # Automatically converted to JSON since returning a dictionary

    def post(self):
        args = self.reqparser.parse_args()  #
        f = {}
        for k, v in args.items():
            f[k] = v
        self.server.files.append(f)
        return {'file': f}

    def put(self):
        pass

    def delete(self):
        pass


#  Created a route at /files with an endpoint called files
api.add_resource(fileListApi, "/files", endpoint="files")


class fileApi(Resource):
    def __init__(self):
        global fileS
        self.server = fileS
        print('server', self.server.files)
        super(fileApi, self).__init__()  # Initialising the Resource class
        self.reqparser = reqparse.RequestParser()  # Init a request parser

        # For every value coming in JSON, you need an argument
        self.reqparser.add_argument('name', type=str, location='json')  # Repeat for multiple variables
        # self.reqparser.add_argument('Client_ID', type=str, location = 'json')  # Repeat for multiple variables

    def get(self, name):
        f = [f for f in self.server.files if f['name'] == name]
        if len(f) == 0:
            return {'success': False}  # Not in the list
        f = f[0]  # Take first element of f (should only be one)
        return {"File": f}
        # return {"Hello": "World"}  # Automatically converted to JSON since returning a dictionary

    def put(self, name):
        f = [f for f in self.server.files if f['name'] == name]
        if len(f) == 0:
            return {'success': False}
        f = f[0]  # Only take the first value
        args = self.reqparser.parse_args()  #
        for k, v in args.items():
            if v != None:
                f[k] = v
        return {'file': f}

    def delete(self, name):
        pass

#  Created a route at /files/'input string' with an endpoint called files
#  The 'input string' is taken as the value "name"
#  This API handles requests such as GET /files/Python3 and PUT {"name":
#  "Javascript"} for /files/Python
api.add_resource(fileApi, "/files/<string:name>", endpoint="file")

class fileServer():
    def __init__(self):
        print ('starting')
        self.files = [{'name':'Javascript'},{'name':'Python'},{'name':'Ruby'}]
        print ('done')

if __name__ == "__main__":
    fileS = fileServer()
    app.run(debug=True)
