from flask import Flask
from flask_restful import Resource, Api, reqparse
import os, sys

#  https://flask-restful.readthedocs.io/en/latest/quickstart.html
#  Use Postman desktop application for testing
#  MongoDB automatically in JSON

app = Flask(__name__)
api = Api(app)

class lockingFileAccess(Resource):
    def __init__(self):  # Upon initialisation of the class
        global fileS  # Init the global server
        self.server = fileS  # Init the global server
        super(lockingFileAccess, self).__init__()  # Initialising the Resource class
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('id', type=int, location='json')  # Repeat for multiple variables

    #  Add the client to the lock list for the file
    def put(self, filename):
        # Polling implementation (Will quickly say true or false, not loop here)
        args = self.reqparser.parse_args()  # parse the arguments from the POST
        if filename in self.server.locks:
            if args['id'] not in self.server.locks[filename]:
                self.server.locks[filename].append(args['id'])
                print("appended client {} to lock list for {}".format(args['id'], filename))
                print(self.server.locks)
                return {'success': 'Acquired'}
            else:
                print("already got that one")
                return {'success': 'Already in list'}  # CLient is already in lock list for
        else:
            print("File not on server")
            return {'success': 'Not on server'}

    #  In order to remove from the list
    def delete(self, filename):
        args = self.reqparser.parse_args()
        if filename not in self.server.locks:  # File not in the lock list
            return {'success': 'Not on list'}
        if args['id'] in self.server.locks[filename]:
            self.server.locks[filename].remove(args['id'])
            print("Lock queue: {}".format(self.server.locks))
            return {'success':'Removed'}

        print("Not on list for some reason")
        return {'success': 'Not on list'}

api.add_resource(lockingFileAccess, "/lock/<string:filename>", endpoint="lock")


class lockingAcquire(Resource):
    def __init__(self):  # Upon initialisation of the class
        global fileS  # Init the global server
        self.server = fileS  # Init the global server
        super(lockingAcquire, self).__init__()  # Initialising the Resource class

    #  Give a unique client ID to the client
    def get(self):
        self.server.currentID += 1
        return {'id':self.server.currentID}


api.add_resource(lockingAcquire, "/lock", endpoint="lockID")

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
        if any(d['filename'] == f['filename'] for d in self.server.files):  # Check if a file with that name exists
            return {'success':False}  # Already in the filesystem
        else:
            self.server.files.append(f)  # append to file list
            self.server.locks[f['filename']] = []  # add to lock list
            print("Created lock buffer for {}\nCurrent Lock list: {}".format(f['filename'], self.server.locks))
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
        self.reqparser.add_argument('clientID', type=int, location='json')
        # self.reqparser.add_argument('Client_ID', type=str, location = 'json')  # Repeat for multiple variables

    def get(self, filename):
        f = [f for f in self.server.files if f['filename'] == filename]
        if len(f) == 0:
            return {'success': False}  # Not in the list
        f = f[0]  # Take first element of f (should only be one)
        return f # f['filename'] to just get the name of the file
        # return {"Hello": "World"}  # Automatically converted to JSON since returning a dictionary

    def delete(self, filename):
        args = self.reqparser.parse_args()  # args is a list containing the new data
        print(args)
        if filename not in self.server.locks:
            return {'success': 'Not in list'}

        if args['clientID'] != self.server.locks[filename][0]:
            return {'success': 'locked'}

        f = [f for f in self.server.files if f['filename'] == filename]
        if len(f) == 0:
            return {'success': 'Not in list'}  # Not in the list
        self.server.files[:] = [d for d in self.server.files if d.get('filename') != filename]
        self.server.locks.pop(filename, 0)
        print("Deleted lock buffer for {}\nCurrent Lock list: {}".format(filename, self.server.locks))

        dir = os.path.dirname(__file__)  # Get full path on the system to the current ActualRESTful.py location
        serverDataPath = os.path.join(dir, 'serverData')  # Append the serverData folder to path
        serverDataPath = os.path.join(serverDataPath, filename)
        print(serverDataPath)

        if os.path.exists(serverDataPath):
            os.remove(serverDataPath)  # Delete the file from server storage
        print(self.server.files)
        return {'success':'Deleted'}

    #  FILENAME IS PASSED FROM ENDPOINT <STRING>
    def put(self, filename):
        args = self.reqparser.parse_args()  # args is a list containing the new data
        print(args)

        if args['clientID'] != self.server.locks[filename][0]:
            return {'success': 'locked'}
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
        self.locks = {}  # Stores all locking data

        dir = os.path.dirname(__file__)  # Get full path on the system to the current ActualRESTful.py location
        filePath = os.path.join(dir, 'serverData')  # Append the serverData folder to path
        print("\nServer files found:\n")
        for fileName in os.listdir(filePath):
            if fileName.endswith(".txt"):  # For each text file in the serverData folder
                print(fileName)
                with open(os.path.join("serverData",fileName), "r") as myfile:
                    data = myfile.readlines()
                self.files.append({'filename':fileName, "data":data, "version":0})
                self.locks[fileName] = []
        print("\n")
        self.currentID = 0


if __name__ == "__main__":
    fileS = fileServer()  # Fill fileS with the init values of class fileServer
    app.run(port=int(sys.argv[1]))
