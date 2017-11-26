from flask import Flask
from flask_restful import Resource, Api, reqparse
import requests, json

app = Flask(__name__)
api = Api(app)

class getFileLocation(Resource):
    def __init__(self):  # Upon initialisation of the class
        global fileS  # Init the global server
        self.server = fileS  # Init the global server
        super(getFileLocation, self).__init__()  # Initialising the Resource class
        self.reqparser = reqparse.RequestParser()

        # For every value coming in JSON, you need an argument
        self.reqparser.add_argument('filename', type=str, location = 'json')  # Repeat for multiple variables
        self.reqparser.add_argument('data', type=str, location='json')
        self.reqparser.add_argument('version', type=int, location='json')

    def get(self, filename):

        # Need to update file lists in case anything has changed
        self.server.serverInfo['fileServer1']['serverFiles'] = []  # reset file lists for checking files
        self.server.serverInfo['fileServer2']['serverFiles'] = []  # reset file lists for checking files
        # file server 1 on port 5001
        # file server 2 on port 5002
        location = 'http://{}:{}/filedir'.format(self.server.serverInfo['fileServer1']['ip'],
                                                 self.server.serverInfo['fileServer1']['port'])
        r = requests.get(location)
        json_data = json.loads(r.text)  # JSON to dict
        print("FILESERVER 1 FILES: {}".format(json_data))

        for x in json_data:
            self.server.serverInfo['fileServer1']['serverFiles'].append(x['filename'])

        location = 'http://{}:{}/filedir'.format('localhost', 5002)
        r = requests.get(location)
        json_data = json.loads(r.text)  # JSON to dict
        print("FILESERVER 2 FILES: {}".format(json_data))

        for x in json_data:
            self.server.serverInfo['fileServer2']['serverFiles'].append(x['filename'])

        # Now that the file lists are up to date, can locate what server the file is on
        for x in self.server.serverInfo['fileServer1']['serverFiles']:
            if x == filename:
                return {'ip':self.server.serverInfo['fileServer1']['ip'],
                        'port':self.server.serverInfo['fileServer1']['port'],
                        'filename':filename}

        for x in self.server.serverInfo['fileServer2']['serverFiles']:
            if x == filename:
                return {'ip':self.server.serverInfo['fileServer2']['ip'],
                        'port':self.server.serverInfo['fileServer2']['port'],
                        'filename':filename}

        print(self.server.serverInfo)
        return {'ip':-1}
        # return {"Hello": "World"}  # Automatically converted to JSON since returning a dictionary

#  Created a route at /files with an endpoint called files
api.add_resource(getFileLocation, "/filedir/<string:filename>", endpoint="file")


class getFileList(Resource):
    def __init__(self):  # Upon initialisation of the class
        global fileS  # Init the global server
        self.server = fileS  # Init the global server
        super(getFileList, self).__init__()  # Initialising the Resource class
        self.reqparser = reqparse.RequestParser()

        # For every value coming in JSON, you need an argument
        self.reqparser.add_argument('filename', type=str, location = 'json')  # Repeat for multiple variables
        self.reqparser.add_argument('data', type=str, location='json')
        self.reqparser.add_argument('version', type=int, location='json')

    def get(self):
        return self.server.serverInfo  # Return the server info

#  Created a route at /files with an endpoint called files
api.add_resource(getFileList, "/filedir", endpoint="filelist")


class getAServer(Resource):
    def __init__(self):  # Upon initialisation of the class
        global fileS  # Init the global server
        self.server = fileS  # Init the global server
        super(getAServer, self).__init__()  # Initialising the Resource class
        self.reqparser = reqparse.RequestParser()

    def get(self):
        # Alternate between servers for creation of files
        if self.server.serverCount == 1:
            self.server.serverCount = 2
            return self.server.serverInfo['fileServer1']
        elif self.server.serverCount == 2:
            self.server.serverCount = 1
            return self.server.serverInfo['fileServer2']

#  Created a route at /files with an endpoint called files
api.add_resource(getAServer, "/getServer", endpoint="getServer")

class fileServer():
    def __init__(self):
        # If time, create directory with files inside and iterate to fill self.files
        # instead of explicit initialisation of files
        self.serverCount = 1

        self.serverInfo = {'fileServer1':{'ip':'localhost', 'port':5001, 'serverFiles':[]},
                           'fileServer2': {'ip': 'localhost', 'port': 5002, 'serverFiles':[]}}
        # file server 1 on port 5001
        # file server 2 on port 5002
        location = 'http://{}:{}/filedir'.format(self.serverInfo['fileServer1']['ip'], self.serverInfo['fileServer1']['port'])
        r = requests.get(location)
        json_data = json.loads(r.text)  # JSON to dict
        print("FILESERVER 1 FILES: {}".format(json_data))

        for x in json_data:
            self.serverInfo['fileServer1']['serverFiles'].append(x['filename'])

        location = 'http://{}:{}/filedir'.format('localhost', 5002)
        r = requests.get(location)
        json_data = json.loads(r.text)  # JSON to dict
        print("FILESERVER 2 FILES: {}".format(json_data))

        for x in json_data:
            self.serverInfo['fileServer2']['serverFiles'].append(x['filename'])

        print(self.serverInfo)

if __name__ == "__main__":
    fileS = fileServer()  # Fill fileS with the init values of class fileServer
    app.run(port=5000, debug=True)  # PORT 5000