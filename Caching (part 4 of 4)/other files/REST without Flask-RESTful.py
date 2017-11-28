from flask import Flask, jsonify, request
from flask_restful import Resource, Api

#  https://flask-restful.readthedocs.io/en/latest/quickstart.html
#  Use Postman desktop application for testing

# r = requests.get()
# r_text = r.json()

app = Flask(__name__)

listOfData = [{'name':'Javascript'},{'name':'Python'},{'name':'Ruby'}]


@app.route('/', methods=['GET'])
def root():
    return jsonify({'message':'Test sentence'})

@app.route('/lang', methods=['GET'])
def returnAll():
    return jsonify({'languages':listOfData})

@app.route('/lang/<string:name>', methods=['GET'])
def returnOne(name):
    #  form list of items with names which match 'name'
    langs = [language for language in listOfData if language['name'] == name]
    return jsonify({'language':langs[0]})

#  POST to add to the list (in reality would use to add to database)
@app.route('/lang', methods=['POST'])
def addOne():
    langdict = {'name':request.json['name']}  # creates a new dictionary with the name
    listOfData.append(langdict)  # add entry to the list
    return jsonify({'languages': listOfData})  # return the new list with the added entry

#  Doing PUT request to localhost:5000/Javascript with JSON content {"name":"Go"}
#  will replace "Javascript" in the list with "Go"

@app.route('/lang/<string:name>', methods=['PUT'])
def editOne(name):
    #  makes a list with all items in listOfData with name which match 'name'
    langs = [language for language in listOfData if language['name'] == name]
    #  lists in Python are copied by reference
    #  updating langs will update listOfData
    langs[0]['name'] = request.json['name']  # update the name to the name passed in the JSON
    #  langs[0] for only the first matched value
    return jsonify({'language': langs[0]})

@app.route('/lang/<string:name>', methods=['DELETE'])
def removeOne(name):
    langs = [language for language in listOfData if language['name'] == name]
    listOfData.remove(langs[0])  # index 0 since only removing one value
    return jsonify({'languages': listOfData})

if __name__ == "__main__":
    app.run(debug=True)
