import requests

#  https://flask-restful.readthedocs.io/en/latest/quickstart.html
# r = requests.get()
# r_text = r.json()

def run():
    r = requests.get('http://localhost:5000/filedir/file1')
    r_text = r.json()
    print(r_text)
    r = requests.put('http://localhost:5000/filedir/file1', json={'filename':'file2','version':10})  ## NEED JSON

if __name__ == "__main__":
    run()
