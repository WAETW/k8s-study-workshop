from flask import Flask, Response, render_template, request
import prometheus_client
from prometheus_client import Counter
import hashlib
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config.update(
    MONGO_HOST='localhost',
    MONGO_PORT=27017,
    MONGO_USERNAME='admin',
    MONGO_PASSWORD='admin',
    MONGO_DBNAME='user'
)
request_counter = Counter('cc', 'A counter') 

@app.route("/", methods=['GET'])
def index():
    request_counter.inc()
    return render_template("index.html")

@app.route("/login", methods=['POST'])
def login():
    username = request.values['username']
    password = request.values['password']
    def password_hash(password):
        sha = hashlib.sha256()
        sha.update(password.encode("utf-8"))
        return sha.hexdigest()
    has_hash = password_hash(password)
    return "Hello " + username + " Hashed password: " + has_hash


@app.route("/metrics", methods=['GET'])
def request_count():
    return Response(prometheus_client.generate_latest(request_counter), mimetype='text/plain')

if __name__ == "__main__":
    app.run(port=5000, debug=True, host='0.0.0.0')