import requests, json

# Returns a dictionary with all files and their data
def listFiles(ip, port):
    location = 'http://{}:{}/filedir'.format(ip, port)
    r = requests.get(location)
    json_data = json.loads(r.text)  # JSON to dict
    print(json_data)
    # return json_data

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

# Takes a dictionary of the file and PUTs it on to the file server with
def fileDataPUT(ip, port, fileDict):
    location = 'http://{}:{}/filedir/{}'.format(ip, port, fileDict['filename'])
    r = requests.put(location, json={'version':fileDict['version'], 'data':fileDict['data']})
