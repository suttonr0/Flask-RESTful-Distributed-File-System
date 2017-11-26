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
    # Directory service access
    location = 'http://{}:{}/filedir/{}'.format(ip, port, filename)
    r = requests.get(location)
    direct_data = json.loads(r.text)  # JSON to dict (JSON)
    if direct_data['ip'] == -1:
        print("(getFile) File does not exist on server")
        return -1

    # File Server access
    location = 'http://{}:{}/filedir/{}'.format(direct_data['ip'], direct_data['port'], direct_data['filename'])
    r = requests.get(location)
    json_data = json.loads(r.text)  # JSON to dict (JSON)
    if 'success' in json_data:
        if json_data['success'] == False:
            print("(getFile) File does not exist on server")
            return -1
    # print("GET file: name {}, version {}, content {}".format(json_data['filename'], json_data['version'], json_data['data']))
    return json_data

# Takes a dictionary of the file, replaces the data with newText and
# PUTs it on to the file server
# Returns -1 if file is behind on version or if it doesn't exist on the server
def editFile(ip, port, fileDict, newText):
    # Directory service access
    location = 'http://{}:{}/filedir/{}'.format(ip, port, fileDict['filename'])
    r = requests.get(location)
    direct_data = json.loads(r.text)  # JSON to dict (JSON)
    if direct_data['ip'] == -1:
        print("(editFile) File does not exist on server")
        return -1

    # Edit the file
    fileDict['data'] = newText
    location = 'http://{}:{}/filedir/{}'.format(direct_data['ip'], direct_data['port'], direct_data['filename'])
    r = requests.put(location, json={'version': fileDict['version'], 'data':fileDict['data']})
    json_data = json.loads(r.text)
    if json_data['success'] == 'notOnServer':
        print("(editFile) File does not exist on server")
    elif json_data['success'] == 'outOfDate':
        print("(editFile) File is behind on version")
        return -1

# Creates a new file called filename with content data (POST)
def createFile(ip, port, filename, data):
    # Get info for a single file server

    # Create the file
    location = 'http://{}:{}/filedir'.format(ip, port)
    r = requests.post(location, json={'filename': filename, 'version': 0, 'data': data})
    json_data = json.loads(r.text)
    if json_data['success'] == False:
        print("(createFile) The file already exists")

# Deletes the file on the server, returns -1 if file not found
def deleteFile(ip, port, filename):
    # Directory service access
    location = 'http://{}:{}/filedir/{}'.format(ip, port, filename)
    r = requests.get(location)
    direct_data = json.loads(r.text)  # JSON to dict (JSON)
    if direct_data['ip'] == -1:
        print("(getFile) File does not exist on server")
        return -1

    # Delete the file
    location = 'http://{}:{}/filedir/{}'.format(direct_data['ip'], direct_data['port'], direct_data['filename'])
    r = requests.delete(location)
    json_data = json.loads(r.text)  # JSON to dict (JSON
    if 'success' in json_data:
        if json_data['success'] == False:
            print("(deleteFile) File does not exist on server")
            return -1
        elif json_data['success'] == True:
            print("Successful deletion")

# Takes a dictionary of file data and prints it
def printFile(fileDict):

    print("--------------------------")
    print("File Name: {}\nVersion Number: {}\nFile Content:\n{}".format(fileDict['filename'], fileDict['version'], ''.join(fileDict['data'])))
    print("--------------------------")