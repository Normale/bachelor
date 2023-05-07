import socket
from kafka import KafkaProducer, KafkaConsumer
import json
import time

KAFKA_BROKER_URL = 'localhost:19092'
TOPIC = "style-transfer"

# Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Send a test message
producer.send(TOPIC, {'message': 'Hello, Kafka!'})
producer.flush()

# Consumer
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER_URL,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print('Waiting for messages...')
for message in consumer:
    print(f"Received message: {message.value}")
    time.sleep(1)
