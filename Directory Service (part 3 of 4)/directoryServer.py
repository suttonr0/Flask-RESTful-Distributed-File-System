from flask import Flask
from flask_restful import Resource, Api, reqparse
import requests, json

app = Flask(__name__)
api = Api(app)



class fileServer():
    def __init__(self):
        # If time, create directory with files inside and iterate to fill self.files
        # instead of explicit initialisation of files
        self.fileMap = []  # Stores all file data
        # file server 1 on port 5001
        # file server 2 on port 5002
        location = 'http://{}:{}/filedir'.format('localhost', 5001)
        r = requests.get(location)
        json_data = json.loads(r.text)  # JSON to dict
        print("FILESERVER 1 FILES: {}".format(json_data))

        location = 'http://{}:{}/filedir'.format('localhost', 5002)
        r = requests.get(location)
        json_data = json.loads(r.text)  # JSON to dict
        print("FILESERVER 2 FILES: {}".format(json_data))

if __name__ == "__main__":
    fileS = fileServer()  # Fill fileS with the init values of class fileServer
    app.run(port=5000, debug=True)  # PORT 5000