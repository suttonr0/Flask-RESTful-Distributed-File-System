import sys, clientLibrary

#  https://flask-restful.readthedocs.io/en/latest/quickstart.html
# r = requests.get()
# r_text = r.json()

def run():

    localCache = []  # To cache files in memory
    ipAddress = sys.argv[1]
    portNumber = int(sys.argv[2])
    print("IP:{} Port:{}".format(ipAddress,portNumber))
    running = True
    while running:
        userChoice = input("Enter the number for the specified action\n"
                           "1. List files, their versions and their data\n"
                           "2. Read a file\n"
                           "3. Write to an existing file\n"
                           "4. Create a new file\n"
                           "5. Delete an existing file\n"
                           "6. Push to server\n"
                           "0. Exit the client application\n")
        if userChoice == '1':
            clientLibrary.listFiles(ipAddress, portNumber, localCache)

        elif userChoice == '2':
            userFile = input("Enter the file name: ")  # must include file extension
            fileRecv = clientLibrary.getFile(ipAddress, portNumber, userFile, localCache)
            if fileRecv != -1:
                clientLibrary.printFile(fileRecv)

        elif userChoice == '3':
            userFile = input("Enter the file name: ")
            fileRecv = clientLibrary.getFile(ipAddress, portNumber, userFile, localCache)
            if fileRecv != -1:
                clientLibrary.printFile(fileRecv)
                dataToWrite = input("Type the text you want to write to the file: ")
                clientLibrary.editFile(fileRecv, dataToWrite, localCache)
            else:
                print("File not found\n")

        elif userChoice == '4':
            userFile = input("Enter the new file name: ")
            userData = input("Enter the new data for the file: ")
            clientLibrary.createFile(ipAddress, portNumber, userFile, userData, localCache)

        elif userChoice == '5':
            userFile = input("Enter the file name to delete: ")
            clientLibrary.deleteFile(ipAddress, portNumber, userFile, localCache)

        elif userChoice == '6':
            userFile = input("Enter the filename to push to the server: ")
            clientLibrary.uploadFile(ipAddress, portNumber, userFile, localCache)

        elif userChoice == '0':
            print("Ending client application")
            running = False


if __name__ == "__main__":
    run()
