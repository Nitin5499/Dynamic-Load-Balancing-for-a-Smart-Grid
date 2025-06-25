# load_balancer/main.py

from flask import Flask, request, jsonify
import requests
import threading
import time
import re

app = Flask(__name__)

# List of substation hostnames from Docker Compose
SUBSTATION_URLS = [
    "http://substation1:5003",
    "http://substation2:5003",
    "http://substation3:5003"
]

# Dictionary to store current load of each substation
substation_loads = {url: 0 for url in SUBSTATION_URLS}


def get_current_load(metrics_text):
    """Extract the load value from the Prometheus metrics text"""
    match = re.search(r'current_load\s+(\d+)', metrics_text)
    return int(match.group(1)) if match else float('inf')


def update_loads():
    """Continuously update the load of each substation every 5 seconds"""
    while True:
        for url in SUBSTATION_URLS:
            try:
                metrics = requests.get(f"{url}/metrics").text
                substation_loads[url] = get_current_load(metrics)
            except Exception:
                substation_loads[url] = float('inf')  # mark as overloaded or unreachable
        time.sleep(5)


@app.route('/assign', methods=['POST'])
def assign_substation():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    # Select substation with lowest load
    least_loaded = min(substation_loads, key=substation_loads.get)

    try:
        response = requests.post(f"{least_loaded}/charge", json=data)
        return jsonify({
            "assigned_substation": least_loaded,
            "substation_response": response.json()
        }), response.status_code
    except Exception as e:
        return jsonify({"error": "Failed to forward to substation", "details": str(e)}), 500


if __name__ == '__main__':
    # Start thread to poll metrics
    thread = threading.Thread(target=update_loads)
    thread.daemon = True
    thread.start()
    
    app.run(host='0.0.0.0', port=5002)


