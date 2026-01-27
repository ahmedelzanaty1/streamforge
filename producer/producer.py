import json
import time
import uuid
import os
from datetime import datetime
from kafka import KafkaProducer

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def generate_trip():
    return {
        "trip_id": str(uuid.uuid4()),
        "distance_km": round(1 + 100 * time.time() % 1, 2),
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    while True:
        trip = generate_trip()
        producer.send(KAFKA_TOPIC, trip)
        print(f"Sent trip: {trip}")
        time.sleep(2)
