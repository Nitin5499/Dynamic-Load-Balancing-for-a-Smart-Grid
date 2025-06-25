# substation_service/main.py

from flask import Flask, request, jsonify
from prometheus_client import start_http_server, Gauge
import threading
import time
import random

app = Flask(__name__)

# Prometheus metric
current_load = Gauge('current_load', 'Current load on substation')

# Shared state
load = 0
lock = threading.Lock()

@app.route('/charge', methods=['POST'])
def charge():
    global load
    with lock:
        load += 1
        current_load.set(load)

    # Simulate charging time
    def simulate_charge():
        global load
        time.sleep(random.randint(5, 10))  # Simulated charging time
        with lock:
            load -= 1
            current_load.set(load)

    threading.Thread(target=simulate_charge).start()
    return jsonify({"status": "Charging started"}), 200


if __name__ == '__main__':
    # Start Prometheus server on default /metrics (port 8000 internally)
    start_http_server(8000)
    app.run(host='0.0.0.0', port=5003)