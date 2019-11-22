from flask import Flask, Response
import prometheus_client
from prometheus_client import Counter

app = Flask(__name__)

request_counter = Counter('cc', 'A counter') 

@app.route("/", methods=['GET'])
def hello():
    request_counter.inc()
    return "Hello, World!"

@app.route("/metrics", methods=['GET'])
def request_count():
    return Response(prometheus_client.generate_latest(request_counter), mimetype='text/plain')

if __name__ == "__main__":
    app.run(port=5000, debug=True, host='0.0.0.0')