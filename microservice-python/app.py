from flask import Flask, jsonify
import logging
from pythonjsonlogger import jsonlogger
import requests
import os

app = Flask(__name__)

SPLUNK_HEC_URL = os.environ.get('SPLUNK_HEC_URL', 'https://localhost:8088/services/collector/event')
SPLUNK_TOKEN = os.environ.get('SPLUNK_TOKEN', 'INSERISCI_IL_TUO_TOKEN')

def send_log_to_splunk(log_msg):
    headers = {"Authorization": f"Splunk {SPLUNK_TOKEN}"}
    payload = {"event": log_msg}
    try:
        response = requests.post(SPLUNK_HEC_URL, headers=headers, json=payload, verify=False)
        # print(f"Splunk response: {response.status_code}")
    except Exception as e:
        print(f"Errore invio log a Splunk: {e}")

# --- Logging enterprise-ready ---
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(levelname)s %(message)s'
)
logHandler.setFormatter(formatter)
app.logger.addHandler(logHandler)
app.logger.setLevel(logging.INFO)

@app.route('/health', methods=['GET'])
def health():
    log_event = {'level': 'INFO', 'message': 'Health check ok', 'endpoint': '/health'}
    app.logger.info('Health check ok', extra={'endpoint': '/health'})
    send_log_to_splunk(log_event)
    return jsonify({'status': 'ok', 'version': 'canary'}), 200

@app.route('/log', methods=['GET'])
def log():
    app.logger.info('Example event log', extra={'event': 'log', 'custom_field': 'test'})
    return jsonify({'log': 'generated', 'version': 'canary'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)