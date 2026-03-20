from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest
import time

app = Flask(__name__)

# Metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total Requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency')

@app.route('/')
def home():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    return jsonify({"message": "Welcome to DevOps App 🚀"})

@app.route('/hello/<name>')
def hello(name):
    REQUEST_COUNT.labels(method='GET', endpoint='/hello').inc()
    return jsonify({"message": f"Hello {name}!"})

@app.route('/data', methods=['POST'])
def data():
    REQUEST_COUNT.labels(method='POST', endpoint='/data').inc()
    start = time.time()
    
    payload = request.json
    time.sleep(0.5)  # simulate processing
    
    REQUEST_LATENCY.observe(time.time() - start)
    
    return jsonify({"received": payload})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
