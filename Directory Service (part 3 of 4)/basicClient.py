import requests, json, clientLibrary

#  https://flask-restful.readthedocs.io/en/latest/quickstart.html
# r = requests.get()
# r_text = r.json()

def run():
    ipAddress = input("Enter the IP of the directory server: ")
    portNumber = input("Enter the port number of the directory server: ")
    print("IP:{} Port:{}".format(ipAddress,portNumber))
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
                dataToWrite = input("Type the text you want to write to the file: ")
                clientLibrary.editFile(ipAddress, portNumber, fileRecv, dataToWrite)
            else:
                print("File not found\n")

        elif userChoice == '4':
            userFile = input("Enter the new file name: ")
            userData = input("Enter the new data for the file: ")
            clientLibrary.createFile(ipAddress, portNumber, userFile, userData)

        elif userChoice == '5':
            userFile = input("Enter the file name to delete: ")
            clientLibrary.deleteFile(ipAddress, portNumber, userFile)

        elif userChoice == '0':
            print("Ending client application")
            running = False

        # clientLibrary.listFiles('127.0.0.1', 5000)
        # firstFile = clientLibrary.getFile('localhost', 5000, 'file1.txt')
        # print(firstFile['data'])
        # if firstFile != -1:
        #     clientLibrary.editFile('localhost', 5000, firstFile, "hello new text here")
        # clientLibrary.createFile('localhost', 5000, 'superfile3.txt', "What a great file")
        # clientLibrary.listFiles('127.0.0.1', 5000)
        # clientLibrary.deleteFile('localhost', 5000, 'file2.txt')
        # clientLibrary.listFiles('127.0.0.1', 5000)

if __name__ == "__main__":
    run()
