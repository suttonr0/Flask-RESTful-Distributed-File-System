import requests, json

# Returns a dictionary with all files and their data
def listFiles(ip, port):
    location = 'http://{}:{}/filedir'.format(ip, port)
    r = requests.get(location)
    json_data = json.loads(r.text)  # JSON to dict
    return json_data

# Takes the dictionary of filename, version and data as fileDict, replaces
# the data with newText, and returns the dictionary
def editFile(fileDict, newText):
    fileDict['data'] = newText
    return fileDict

# Returns a dictionary with the file name, version number and file content for the filename
# passed on the fileserver with provided port and ip
def fileDataGET(ip, port, filename):
    location = 'http://{}:{}/filedir/{}'.format(ip, port, filename)
    r = requests.get(location)
    json_data = json.loads(r.text)  # JSON to dict (JSON
    print("GET file: name {}, version {}, content {}".format(json_data['filename'], json_data['version'], json_data['data']))
    return json_data

def fileDataPUT(ip, port, filename, data):
    location = 'http://{}:{}/filedir/{}'.format(ip, port, filename)
    r = requests.put('http://localhost:5000/filedir/file2.txt', json={'version':10, 'data':out_text})
