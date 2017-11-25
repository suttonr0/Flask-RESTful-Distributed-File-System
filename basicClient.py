import requests, json, clientLibrary

#  https://flask-restful.readthedocs.io/en/latest/quickstart.html
# r = requests.get()
# r_text = r.json()

def run():
    clientLibrary.listFiles('127.0.0.1', 5000)
    firstFile = clientLibrary.fileDataGET('localhost', 5000, 'file1.txt')
    firstFile = clientLibrary.editFile(firstFile, "hello new text here")
    print(firstFile['data'])

    # out_text = "Why hello there what a nice evening"
    # r = requests.put('http://localhost:5000/filedir/file2.txt', json={'version':10, 'data':out_text})  ## NEED JSON

if __name__ == "__main__":
    run()
