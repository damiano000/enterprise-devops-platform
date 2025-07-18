from flask import Flask, jsonify
import logging
from pythonjsonlogger import jsonlogger

app = Flask(__name__)

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
    app.logger.info('Health check OK', extra={'endpoint': '/health'})
    return jsonify({'status': 'ok'}), 200

@app.route('/log', methods=['GET'])
def log():
    app.logger.info('Example event log', extra={'event': 'log', 'custom_field': 'test'})
    return jsonify({'log': 'generated'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)