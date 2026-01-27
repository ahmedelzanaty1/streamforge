import json
import os
import psycopg2
from kafka import KafkaConsumer

# Kafka config
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

# Postgres config
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Kafka consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

# Postgres connection
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()

print("Consumer started. Waiting for messages...")

for message in consumer:
    trip = message.value
    distance = trip.get("distance_km", 0)

    if distance > 10:
        cursor.execute(
            """
            INSERT INTO trips (trip_id, distance_km, timestamp)
            VALUES (%s, %s, %s)
            """,
            (trip["trip_id"], distance, trip["timestamp"])
        )
        conn.commit()
        print(f"Stored trip: {trip}")
