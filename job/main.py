import os
import random
import time
import uuid

from confluent_kafka import SerializingProducer
import simplejson as json
from datetime import datetime, timedelta
from producer import *

# Environment Variables for configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
ORDER_TOPIC = os.getenv('ORDER_TOPIC', 'order_data')
STATUS_TOPIC = os.getenv('STATUS_TOPIC', 'status_data')
REVIEW_TOPIC = os.getenv('REVIEW_TOPIC', 'review_data')

start_time = datetime.now()

random.seed(42)

def get_next_time():
    global start_time
    start_time += timedelta(seconds=random.randint(30, 60))  # update frequency
    return start_time

def generate_order_data(order_id):
    return {
        'id': order_id,
        'customerId': str(uuid.uuid4()),
        'timestamp': get_next_time().isoformat(),
        'items': [{'itemId': str(uuid.uuid4()), 'quantity': random.randint(1, 5)} for _ in range(random.randint(1, 5))],
        'totalPrice': round(random.uniform(10, 100), 2)
    }

def generate_status_data(order_id):
    return {
        'id': order_id,
        'timestamp': get_next_time().isoformat(),
        'status': random.choice(['Received', 'Preparing', 'Ready for Pickup', 'Out for Delivery', 'Delivered'])
    }

def generate_review_data(order_id):
    return {
        'id': order_id,
        'timestamp': get_next_time().isoformat(),
        'rating': random.randint(1, 5),
        'comments': random.choice(['Excellent', 'Good', 'Average', 'Poor', 'Terrible'])
    }

def simulate_orders(producer):
    while True:
        order_id = str(uuid.uuid4())
        order_data = generate_order_data(order_id)
        status_data = generate_status_data(order_id)
        review_data = generate_review_data(order_id)

        produce_data_to_kafka(producer, ORDER_TOPIC, order_data)
        produce_data_to_kafka(producer, STATUS_TOPIC, status_data)
        produce_data_to_kafka(producer, REVIEW_TOPIC, review_data)

        time.sleep(5)

if __name__ == "__main__":
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'error_cb': lambda err: print(f'Kafka error: {err}'),
        'security.protocol': 'PLAINTEXT'
    }
    producer = SerializingProducer(producer_config)

    try:
        simulate_orders(producer)
    except KeyboardInterrupt:
        print('Simulação finalizada pelo usuário')
    except Exception as e:
        print(f"Erro inesperado ocorreu: {e}")