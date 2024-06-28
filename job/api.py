from flask import Flask, request, jsonify
from confluent_kafka import SerializingProducer
import os
import uuid
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# Environment Variables for configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
STATUS_TOPIC = os.getenv('STATUS_TOPIC', 'status_data')
REVIEW_TOPIC = os.getenv('REVIEW_TOPIC', 'review_data')

producer_config = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'error_cb': lambda err: print(f'Kafka error: {err}'),
    'security.protocol': 'PLAINTEXT'
}
producer = SerializingProducer(producer_config)

def produce_data_to_kafka(producer, topic, data):
    producer.produce(topic, key=str(uuid.uuid4()), value=json.dumps(data))
    producer.flush()

@app.route('/status', methods=['POST'])
def send_status():
    data = request.json
    produce_data_to_kafka(producer, STATUS_TOPIC, data)
    return jsonify({"message": "Status data sent to Kafka"}), 200

@app.route('/review', methods=['POST'])
def send_review():
    data = request.json
    produce_data_to_kafka(producer, REVIEW_TOPIC, data)
    return jsonify({"message": "Review data sent to Kafka"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)