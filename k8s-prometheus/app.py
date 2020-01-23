from flask import Flask, Response, render_template, request
import prometheus_client
from prometheus_client import Counter
import hashlib
import json
from flask_pymongo import PyMongo
import os
app = Flask(__name__)

mongodb_host = os.environ.get('MONGODB_SVC_PORT_27017_TCP_ADDR')
app.config.update(
    MONGO_HOST = mongodb_host,
    MONGO_PORT = 27017,
    MONGO_USERNAME = 'admin',
    MONGO_PASSWORD = 'admin',
    MONGO_DBNAME = 'user'
)
app.config["MONGO_URI"] = "mongodb://" + mongodb_host + ":27017/user"
mongo = PyMongo(app)
request_counter = Counter('cc', 'A counter') 

def password_hash(password):
        sha = hashlib.sha256()
        sha.update(password.encode("utf-8"))
        return sha.hexdigest()

@app.route("/", methods=['GET'])
def index():
    request_counter.inc()
    return render_template("index.html")

@app.route("/login", methods=['POST'])
def login():
    username = request.values['username']
    password = request.values['password']
    has_hash = password_hash(password)
    user = mongo.db.users.find_one({'username':username, 'password':has_hash})
    if user != None:
        return "Hello " + username
    else:
        return "No user find!!!"

@app.route("/signup", methods=['POST'])
def signup():
    username = request.values['username']
    password = request.values['password']
    has_hash = password_hash(password)
    user = {
        'username':username,
        'password':has_hash,
    }
    mongo.db.users.insert_one(user)
    return "Thank for signing up! Username: " + username 
@app.route("/metrics", methods=['GET'])
def request_count():
    return Response(prometheus_client.generate_latest(request_counter), mimetype='text/plain')

if __name__ == "__main__":
    app.run(port=5000, debug=True, host='0.0.0.0')