import requests


#  https://flask-restful.readthedocs.io/en/latest/quickstart.html

def run():
    r = requests.get('http://localhost:5000/files')
    r_text = r.json()
    print(r_text)


if __name__ == "__main__":
    run()
