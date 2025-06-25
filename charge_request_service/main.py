
from prometheus_client import Gauge
from prometheus_client import start_http_server
from flask import Flask, request, jsonify
import requests
import threading
import random 
import time


app = Flask(__name__)

# Replace with your actual load balancer URL
LOAD_BALANCER_URL = "http://load_balancer:5002/dispatch"

@app.route('/charge', methods=['POST'])
def charge():
    # Forward the request to the load balancer
    data = request.json
    try:
        response = requests.post(LOAD_BALANCER_URL, json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return "Charge Request Service is running!"
app = Flask(__name__)

current_load = Gauge('current_load', 'Current load on the substation')

def load_simulator():
    while True:
        current_load.set(random.randint(10, 100))
        time.sleep(5)

@app.route('/')
def index():
    return "Substation is running."

if __name__ == "__main__":
    # Start Prometheus metrics server
    start_http_server(8000)
    
    # Start the simulator thread
    threading.Thread(target=load_simulator, daemon=True).start()
    
    # Start the Flask app
    app.run(host="0.0.0.0", port=5003)