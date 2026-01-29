import json
import time
import uuid
import os
import random
from datetime import datetime
from kafka import KafkaProducer

# ENV variables
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

def generate_trip():
    return {
        "trip_id": str(uuid.uuid4()),
        "distance_km": round(random.uniform(5, 50), 2),
        "timestamp": datetime.utcnow().isoformat()
    }

# Connect to Kafka with retry loop
while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        print("Kafka producer connected")
        break
    except Exception as e:
        print(f"Kafka broker not available yet: {e}")
        time.sleep(5)

# Produce messages indefinitely
print("Producer started. Sending trips...")
while True:
    trip = generate_trip()
    try:
        producer.send(KAFKA_TOPIC, trip)
        producer.flush()
        print(f"Sent trip: {trip}")
    except Exception as e:
        print(f"Failed to send trip: {e}")
    time.sleep(2)
