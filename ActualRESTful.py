from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse

#  https://flask-restful.readthedocs.io/en/latest/quickstart.html
#  Use Postman desktop application for testing
#  MongoDB automatically in JSON

app = Flask(__name__)  ## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
api = Api(app)  ## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

#  API for dealing with the list of files as a whole
class fileListApi(Resource):
    def __init__(self):  # Upon initialisation of the class
        global fileS  # Init the global server
        self.server = fileS  # Init the global server
        super(fileListApi, self).__init__()  # Initialising the Resource class
        self.reqparser = reqparse.RequestParser()

        # For every value coming in JSON, you need an argument
        self.reqparser.add_argument('filename', type=str, location = 'json')  # Repeat for multiple variables
        self.reqparser.add_argument('data', type=str, location='json')  # Repeat for multiple variables
        self.reqparser.add_argument('version', type=int, location='json')  # Repeat for multiple variables
        # e.g to add a client_ID value do:
        # self.reqparser.add_argument('client_ID', type=str, location = 'json')  # Repeat for multiple variables

    def get(self):
        return {"Files": self.server.files}
        # return {"Hello": "World"}  # Automatically converted to JSON since returning a dictionary

    #  Creating new file data
    def post(self):
        args = self.reqparser.parse_args()  #
        f = {}
        for k, v in args.items():
            f[k] = v
        self.server.files.append(f)
        return {'file': f}

#  Created a route at /files with an endpoint called files
api.add_resource(fileListApi, "/filedir", endpoint="filelist")  ## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


#  API for dealing with individual files
class fileApi(Resource):
    def __init__(self):
        global fileS
        self.server = fileS
        super(fileApi, self).__init__()  # Initialising the Resource class
        self.reqparser = reqparse.RequestParser()  # Init a request parser
        # For every value coming in JSON, you need an argument
        self.reqparser.add_argument('filename', type=str, location='json')  # Repeat for multiple variables
        self.reqparser.add_argument('data', type=str, location='json')  # Repeat for multiple variables
        self.reqparser.add_argument('version', type=int, location='json')
        # self.reqparser.add_argument('Client_ID', type=str, location = 'json')  # Repeat for multiple variables

    def get(self, filename):
        f = [f for f in self.server.files if f['filename'] == filename]
        if len(f) == 0:
            return {'success': False}  # Not in the list
        f = f[0]  # Take first element of f (should only be one)
        print(f)

        return f # f['filename'] to just get the name of the file
        # return {"Hello": "World"}  # Automatically converted to JSON since returning a dictionary

    #  FILENAME IS PASSED FROM ENDPOINT <STRING>
    def put(self, filename):
        args = self.reqparser.parse_args()  # args is a list containing
        print("hi")
        print(args['version'])
        # f = [f for f in self.server.files if f['filename'] == filename]
        # if len(f) == 0:
        #     return {'success': False}
        # f = f[0]  # Only take the first value
        # args = self.reqparser.parse_args()  # args is a list containing
        # print(args)
        # for k, v in args.items():
        #     if v != None:
        #        print(v)
        #         f[k] = v
        # return {'file': f}
        return {"success":True}

#  Created a route at /files/'input string' with an endpoint called files
#  The 'input string' is taken as the value "name"
#  This API handles requests such as GET /files/Python3 and PUT {"name":
#  "Javascript"} for /files/Python
api.add_resource(fileApi, "/filedir/<string:filename>", endpoint="file")  ## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


class fileServer():
    def __init__(self):
        with open("file1.txt", "r") as myfile:
            data1 = myfile.readlines()

        with open("file2.txt", "r") as myfile:
            data2 = myfile.readlines()

        counter = 0
        counter2 = 0

        print(data1)
        #  Init files
        self.files = [{'filename':'file1', "data":data1, "version":counter},
                      {'filename':'file2', "data":data2, "version":counter2}]

if __name__ == "__main__":  ## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    fileS = fileServer()  # Fill fileS with the init values of class fileServer
    app.run(debug=True)  ## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
