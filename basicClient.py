import requests, json, clientLibrary

#  https://flask-restful.readthedocs.io/en/latest/quickstart.html
# r = requests.get()
# r_text = r.json()

def run():
    clientLibrary.listFiles('127.0.0.1', 5000)
    firstFile = clientLibrary.getFile('localhost', 5000, 'file1.txt')
    print(firstFile['data'])
    if firstFile != -1:
        clientLibrary.editFile('localhost', 5000, firstFile, "hello new text here")
    clientLibrary.createFile('localhost', 5000, 'superfile3.txt', "What a great file")
    clientLibrary.listFiles('127.0.0.1', 5000)
    clientLibrary.deleteFile('localhost', 5000, 'file2.txt')
    clientLibrary.listFiles('127.0.0.1', 5000)

if __name__ == "__main__":
    run()
