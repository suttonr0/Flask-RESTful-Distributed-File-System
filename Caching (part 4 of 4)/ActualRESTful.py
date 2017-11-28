from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import os

#  https://flask-restful.readthedocs.io/en/latest/quickstart.html
#  Use Postman desktop application for testing
#  MongoDB automatically in JSON

app = Flask(__name__)
api = Api(app)

#  API for dealing with the list of files as a whole
class fileListApi(Resource):
    def __init__(self):  # Upon initialisation of the class
        global fileS  # Init the global server
        self.server = fileS  # Init the global server
        super(fileListApi, self).__init__()  # Initialising the Resource class
        self.reqparser = reqparse.RequestParser()

        # For every value coming in JSON, you need an argument
        self.reqparser.add_argument('filename', type=str, location = 'json')  # Repeat for multiple variables
        self.reqparser.add_argument('data', type=str, location='json')
        self.reqparser.add_argument('version', type=int, location='json')

    def get(self):
        return self.server.files
        # return {"Hello": "World"}  # Automatically converted to JSON since returning a dictionary

    #  Creating new file data and adding it to the list
    def post(self):
        args = self.reqparser.parse_args()  # parse the arguments from the POST
        f = {}
        for k, v in args.items():
            f[k] = v
        if f in self.server.files:
            return {'success':False}  # Already in the filesystem
        else:
            self.server.files.append(f)  # append to file list
            # Write to disk
            dir = os.path.dirname(__file__)  # Get full path on the system to the current ActualRESTful.py location
            serverDataPath = os.path.join(dir, 'serverData')  # Append the serverData folder to path
            serverDataPath = os.path.join(serverDataPath, f['filename'])
            print(serverDataPath)
            currentFile = open(serverDataPath, 'w')
            currentFile.write(f['data'])
            currentFile.close()
            return {'success':True}

#  Created a route at /files with an endpoint called files
api.add_resource(fileListApi, "/filedir", endpoint="filelist")


#  API for dealing with individual files
class fileApi(Resource):
    def __init__(self):
        global fileS
        self.server = fileS
        super(fileApi, self).__init__()  # Initialising the Resource class
        self.reqparser = reqparse.RequestParser()  # Init a request parser
        # For every value coming in JSON, you need an argument
        self.reqparser.add_argument('filename', type=str, location='json')  # Repeat for multiple variables
        self.reqparser.add_argument('version', type=int, location='json')
        self.reqparser.add_argument('data', type=str, location='json')
        # self.reqparser.add_argument('Client_ID', type=str, location = 'json')  # Repeat for multiple variables

    def get(self, filename):
        f = [f for f in self.server.files if f['filename'] == filename]
        if len(f) == 0:
            return {'success': False}  # Not in the list
        f = f[0]  # Take first element of f (should only be one)
        return f # f['filename'] to just get the name of the file
        # return {"Hello": "World"}  # Automatically converted to JSON since returning a dictionary

    def delete(self, filename):
        f = [f for f in self.server.files if f['filename'] == filename]
        if len(f) == 0:
            return {'success': False}  # Not in the list
        self.server.files[:] = [d for d in self.server.files if d.get('filename') != filename]

        dir = os.path.dirname(__file__)  # Get full path on the system to the current ActualRESTful.py location
        serverDataPath = os.path.join(dir, 'serverData')  # Append the serverData folder to path
        serverDataPath = os.path.join(serverDataPath, filename)
        print(serverDataPath)

        if os.path.exists(serverDataPath):
            os.remove(serverDataPath)  # Delete the file from server storage
        print(self.server.files)
        return {'success':True}

    #  FILENAME IS PASSED FROM ENDPOINT <STRING>
    def put(self, filename):
        args = self.reqparser.parse_args()  # args is a list containing the new data
        print(args)
        # print(args['version'])
        f = [f for f in self.server.files if f['filename'] == filename]
        if len(f) == 0:
            return {'success': 'notOnServer'}
        f = f[0]  # Only take the first value.
        # f now contains the JSON data for the filename passed through the endpoint <string>
        # Check version
        if args['version'] < f['version']:
            return {'success':'outOfDate'}

        args['version'] = args['version'] + 1  # increment version number

        # For each argument in the JSON object update the file stored in memory
        for k, v in args.items():
             if v != None:
                print(v)
                f[k] = v

        dir = os.path.dirname(__file__)  # Get full path on the system to the current ActualRESTful.py location
        serverDataPath = os.path.join(dir, 'serverData')  # Append the serverData folder to path
        serverDataPath = os.path.join(serverDataPath, f['filename'])
        print(serverDataPath)
        # Update file data on disk
        currentFile = open(serverDataPath, 'w')
        currentFile.write(f['data'])
        currentFile.close()
        print(f)
        return {'success':f}


#  Created a route at /files/'input string' with an endpoint called files
#  The 'input string' is taken as the value "name"
#  This API handles requests such as GET /files/Python3 and PUT {"name":
#  "Javascript"} for /files/Python
api.add_resource(fileApi, "/filedir/<string:filename>", endpoint="file")


class fileServer():
    def __init__(self):
        # If time, create directory with files inside and iterate to fill self.files
        # instead of explicit initialisation of files
        self.files = []  # Stores all file data

        dir = os.path.dirname(__file__)  # Get full path on the system to the current ActualRESTful.py location
        filePath = os.path.join(dir, 'serverData')  # Append the serverData folder to path
        print(filePath)
        for fileName in os.listdir(filePath):
            if fileName.endswith(".txt"):  # For each text file in the serverData folder
                print(os.path.join("serverData", fileName))
                with open(os.path.join("serverData", fileName), "r") as myfile:
                    data = myfile.readlines()
                self.files.append({'filename': fileName, "data": data, "version": 0})

        print(self.files)


if __name__ == "__main__":
    fileS = fileServer()  # Fill fileS with the init values of class fileServer
    app.run(port=5000, debug=True)
