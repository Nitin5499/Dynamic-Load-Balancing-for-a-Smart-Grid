from flask import Flask, request, jsonify
from prometheus_client import Gauge, generate_latest
import time
import threading

app = Flask(__name__)

# Track current load
current_load = Gauge('current_load', 'Current charging load at the substation')

@app.route('/charge', methods=['POST'])
def charge():
    current_load.inc()  # Increase load
    def process():
        time.sleep(5)  # Simulate charging time
        current_load.dec()  # Decrease load
    threading.Thread(target=process).start()
    return jsonify({"message": "Charging started"}), 202

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
