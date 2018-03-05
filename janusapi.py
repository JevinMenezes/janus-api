import logging

from flask import Flask,jsonify,request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'lunadb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/lunadb'

mongo = PyMongo(app)

@app.route("/", methods=['POST','GET'])
def index():
    if request.method == 'GET':
        return "Home Page" #should provide a list of APIs that are served
    else:
        return "Home Page (using POST request)"

@app.route("/login/<int:id>", methods=['POST','GET'])
def login(id):
    users = mongo.db.users
    obj = users.find_one({'id' : id})
    if obj == None:
        return jsonify({'status' : 200, 'message' : "user doesn't exist"})
    else:
        return jsonify({'name': obj['username'], 'pwd': obj['pwd']})

@app.errorhandler(404)
def not_found(error=None):
    return jsonify({'status': 404, 'message': 'Not Found: ' + request.url})

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == "__main__":
    app.run(debug=True)
