from flask import Flask, Response, render_template
import prometheus_client
from prometheus_client import Counter

app = Flask(__name__)

request_counter = Counter('cc', 'A counter') 

@app.route("/", methods=['GET'])
def index():
    request_counter.inc()
    return render_template("index.html")

@app.route("/metrics", methods=['GET'])
def request_count():
    return Response(prometheus_client.generate_latest(request_counter), mimetype='text/plain')

if __name__ == "__main__":
    app.run(port=5000, debug=True, host='0.0.0.0')