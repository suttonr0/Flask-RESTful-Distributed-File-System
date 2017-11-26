import requests, json, clientLibrary, time

#  https://flask-restful.readthedocs.io/en/latest/quickstart.html
# r = requests.get()
# r_text = r.json()

def run():
    # ipAddress = input("Enter the IP of the fileserver: ")
    # portNumber = input("Enter the port number of the fileserver: ")
    ipAddress = 'localhost'
    portNumber = 5000
    print("IP:{} Port:{}".format(ipAddress,portNumber))

    # Acquire Client ID
    clientID = clientLibrary.lockGetId('localhost', 5000)

    running = True
    while running:
        userChoice = input("Enter the number for the specified action\n"
                           "1. List files, their versions and their data\n"
                           "2. Read a file\n"
                           "3. Write to an existing file\n"
                           "4. Create a new file\n"
                           "5. Delete an existing file\n"
                           "0. Exit the client application\n")
        if userChoice == '1':
            clientLibrary.listFiles(ipAddress,portNumber)

        elif userChoice == '2':
            userFile = input("Enter the file name: ")  # must include file extension
            fileRecv = clientLibrary.getFile(ipAddress, portNumber, userFile)
            if fileRecv != -1:
                clientLibrary.printFile(fileRecv)

        elif userChoice == '3':
            userFile = input("Enter the file name: ")
            fileRecv = clientLibrary.getFile(ipAddress, portNumber, userFile)
            if fileRecv != -1:
                clientLibrary.printFile(fileRecv)
                clientLibrary.lockAddToQueue(ipAddress, portNumber, clientID, userFile)  # Join lock queue

                lockStatus = -1
                while lockStatus == -1:  # Polling
                    dataToWrite = input("Type the text you want to write to the file: ")
                    lockStatus = clientLibrary.editFile(ipAddress, portNumber, clientID, fileRecv, dataToWrite)
                    if lockStatus != -1:
                        break
                    if input("Type '0' to abort edit. Type anything else to wait:") == '0':
                        break
                    time.sleep(2)
                clientLibrary.lockDeleteFromQueue(ipAddress, portNumber, clientID, userFile)  # Leave lock queue
            else:
                print("File not found\n")

        elif userChoice == '4':
            userFile = input("Enter the new file name: ")
            userData = input("Enter the new data for the file: ")
            clientLibrary.createFile(ipAddress, portNumber, userFile, userData)

        elif userChoice == '5':
            userFile = input("Enter the file name to delete: ")
            clientLibrary.lockAddToQueue(ipAddress, portNumber, clientID, userFile)  # Join lock queue
            lockStatus = -1
            while lockStatus == -1:  # Polling
                lockStatus = clientLibrary.deleteFile(ipAddress, portNumber, clientID, userFile)
                if lockStatus != -1:
                    break
                if input("Type '0' to abort deletion. Type anything else to wait:") == '0':
                    break
                time.sleep(2)
            clientLibrary.lockDeleteFromQueue(ipAddress, portNumber, clientID, userFile)  # Leave lock queue

        elif userChoice == '0':
            print("Ending client application")
            running = False


if __name__ == "__main__":
    run()
