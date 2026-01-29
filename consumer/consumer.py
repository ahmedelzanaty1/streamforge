import os
import json
import time
import psycopg2
from kafka import KafkaConsumer

# ENV variables
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Connect to DB
while True:
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        cur = conn.cursor()
        print("Database connected")
        break
    except Exception as e:
        print(f"DB not ready: {e}")
        time.sleep(5)

# Connect to Kafka
while True:
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id="trip-consumer",
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )
        print("Kafka consumer connected")
        break
    except Exception as e:
        print(f"Kafka broker not available yet: {e}")
        time.sleep(5)

# Consume messages indefinitely
print("Consumer started. Waiting for messages...")
for message in consumer:
    trip = message.value
    if trip["distance_km"] > 1:
        cur.execute(
            """
            INSERT INTO trips (trip_id, distance_km, timestamp)
            VALUES (%s, %s, %s)
            """,
            (trip["trip_id"], trip["distance_km"], trip["timestamp"]),
        )
        conn.commit()
        print(f"Stored trip: {trip}")
