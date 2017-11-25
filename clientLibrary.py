import requests, json

# Prints a dictionary with all files and their data
def listFiles(ip, port):
    location = 'http://{}:{}/filedir'.format(ip, port)
    r = requests.get(location)
    json_data = json.loads(r.text)  # JSON to dict
    print("List of files on file server:\n")
    for x in json_data:
        # ''.join(x['data']) to concatenate the strings in the list form fopen
        print("--------------------------")
        print("File Name: {}\nVersion Number: {}\nFile Content:\n{}".format(x['filename'], x['version'], ''.join(x['data'])))
        print("--------------------------")

# Returns a dictionary with the file name, version number and file content for the filename
# passed on the fileserver with provided port and ip
# If the file does not exist, returns -1
def getFile(ip, port, filename):
    location = 'http://{}:{}/filedir/{}'.format(ip, port, filename)
    r = requests.get(location)
    json_data = json.loads(r.text)  # JSON to dict (JSON
    if 'success' in json_data:
        if json_data['success'] == False:
            print("(Get) File does not exist on server")
            return -1
    print("GET file: name {}, version {}, content {}".format(json_data['filename'], json_data['version'], json_data['data']))
    return json_data

# Takes a dictionary of the file, replaces the data with newText and
# PUTs it on to the file server
# Returns -1 if file is behind on version
def editFile(ip, port, fileDict, newText):
    fileDict['data'] = newText
    location = 'http://{}:{}/filedir/{}'.format(ip, port, fileDict['filename'])
    r = requests.put(location, json={'version': fileDict['version'], 'data':fileDict['data']})
    json_data = json.loads(r.text)
    if json_data['success'] == 'notOnServer':
        print("(Edit) File does not exist on server")
    elif json_data['success'] == 'outOfDate':
        print("(Edit) File is behind on version")
        return -1

# Creates a new file called filename with content data (POST)
def createFile(ip, port, filename, data):
    location = 'http://{}:{}/filedir'.format(ip, port)
    r = requests.post(location, json={'filename': filename, 'version': 0, 'data': data})
    json_data = json.loads(r.text)
    if json_data['success'] == False:
        print("(Create) We've already got that file. It hasn't been added")

# Deletes the file on the server, returns -1 if file not found
def deleteFile(ip, port, filename):
    location = 'http://{}:{}/filedir/{}'.format(ip, port, filename)
    r = requests.delete(location)
    json_data = json.loads(r.text)  # JSON to dict (JSON
    if 'success' in json_data:
        if json_data['success'] == False:
            print("(Delete) File does not exist on server")
            return -1
