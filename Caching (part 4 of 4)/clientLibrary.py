import requests, json

# Prints a dictionary with all files and their data
def listFiles(ip, port, clientCache):
    location = 'http://{}:{}/filedir'.format(ip, port)
    r = requests.get(location)
    json_data = json.loads(r.text)  # JSON to dict
    print("List of files on file server:\n")
    for x in json_data:
        # ''.join(x['data']) to concatenate the strings in the list form fopen
        print("--------------------------")
        print("File Name: {}\nVersion Number: {}\nFile Content:\n{}".format(x['filename'], x['version'], ''.join(x['data'])))
        print("--------------------------")

    print("List of files in cache:\n")
    for x in clientCache:
        print("--------------------------")
        print("File Name: {}\nVersion Number: {}\nFile Content:\n{}".format(x['filename'], x['version'], ''.join(x['data'])))
        print("--------------------------")

# Returns a dictionary with the file name, version number and file content for the filename
# passed on the fileserver with provided port and ip
# If the file does not exist, returns -1
def getFile(ip, port, filename, clientCache):
    # REPLACE SO THAT IF IT IS IN CACHE, YOU GET IT FROM THERE
    # OTHERWISE GET IT FROM THE SERVER
    f = [f for f in clientCache if f['filename'] == filename]  # check if in cache

    if len(f) == 0:  # not in cache yet
        print("(getFile) Not in cache")
        # Get from fileserver
        location = 'http://{}:{}/filedir/{}'.format(ip, port, filename)
        r = requests.get(location)
        json_data = json.loads(r.text)  # JSON to dict (JSON
        if 'success' in json_data:
            if json_data['success'] == False:
                print("(getFile) File does not exist on server")
                return -1
        # Store it in the local cache
        clientCache.append(json_data)

    else:  # replace old cached value (could give option)
        print("(getFile) Found in cache")
        f = f[0]  # To turn f from a list of a single dictionary to a single dictionary
        print(f)
        return f

    print(json_data)
    return json_data


# Takes a dictionary of the file, replaces the data with newText and
# PUTs it on to the file server
# Returns -1 if file is behind on version
def editFile(fileData, newText, clientCache):
    #  To edit the file, only the cached version will be changed
    f = [f for f in clientCache if f['filename'] == fileData['filename']]  # check if in cache
    f = f[0]
    if len(f) == 0:  # not in cache yet
        print("(Edit file) File not in cache")
    f['data'] = newText  # Edit cached version
    print(clientCache)


def uploadFile(ip, port, filename, clientCache):
    # uploads file from the cache
    location = 'http://{}:{}/filedir/{}'.format(ip, port, filename)
    f = [f for f in clientCache if f['filename'] == filename]  # check if in cache
    if len(f) == 0:  # not in cache yet
        print("(Upload file) File not in cache")
        return
    f = f[0]
    r = requests.put(location, json={'version': f['version'], 'data':f['data']})
    json_data = json.loads(r.text)
    if json_data['success'] == 'notOnServer':
        print("(editFile) File does not exist on server")
    elif json_data['success'] == 'outOfDate':
        print("(editFile) File is behind on version. Get the updated version")
        # Remove file from cache so that the next time it is accessed, it is from the fileserver and not the cache
        clientCache.remove(f)
        print("{} removed from cache".format(f['filename']))
        return -1

# Creates a new file called filename with content data (POST)
def createFile(ip, port, filename, data, clientCache):
    location = 'http://{}:{}/filedir'.format(ip, port)
    r = requests.post(location, json={'filename': filename, 'version': 0, 'data': data})
    json_data = json.loads(r.text)
    if json_data['success'] == False:
        print("(createFile) The file already exists")
        return
    # Need to add to cache
    clientCache.append({'filename': filename, 'version': 0, 'data': data})

# Deletes the file on the server, returns -1 if file not found
def deleteFile(ip, port, filename, clientCache):
    location = 'http://{}:{}/filedir/{}'.format(ip, port, filename)
    r = requests.delete(location)
    json_data = json.loads(r.text)  # JSON to dict (JSON
    if 'success' in json_data:
        if json_data['success'] == False:
            print("(deleteFile) File does not exist on server")
            return -1
        elif json_data['success'] == True:
            print("Successful deletion")
    # Need to remove from cache
    f = [f for f in clientCache if f['filename'] == filename]
    f = f[0]
    clientCache.remove(f)

# Try to print from cache first
def printFile(fileDict):

    print("--------------------------")
    print("File Name: {}\nVersion Number: {}\nFile Content:\n{}".format(fileDict['filename'], fileDict['version'], ''.join(fileDict['data'])))
    print("--------------------------")
