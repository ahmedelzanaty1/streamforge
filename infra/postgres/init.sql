CREATE TABLE IF NOT EXISTS trips (
    id SERIAL PRIMARY KEY,
    trip_id VARCHAR(64),
    distance_km FLOAT,
    timestamp TIMESTAMP
);
