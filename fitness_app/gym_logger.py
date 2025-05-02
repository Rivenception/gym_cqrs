#pip install confluent_kafka cassandra-driver
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from confluent_kafka import Consumer, KafkaError
import json
import random
import time
from datetime import datetime

# Cassandra configuration
cassandra_cluster = Cluster(
    ['127.0.0.1'],  # Localhost (change if your IP is different)
    port=9042  # Default Cassandra port
)
session = cassandra_cluster.connect('fitness_app')  # Connect to the keyspace
# Kafka configuration (also try localhost:9092 is 9093 doesn't work)
kafka_conf = {
    'bootstrap.servers': 'localhost:9093',
    'group.id': 'gym_log_consumer',
    'auto.offset.reset': 'earliest'
}

# Initialize Consumer
consumer = Consumer(kafka_conf)
consumer.subscribe(['gym'])

def project_into_cassandra(event_data):

    created_at = datetime.utcnow()

    """Inserts the event data into Cassandra."""
    cql = """
    INSERT INTO gym_alerts (member_name, created_at, check_in_time, check_out_time, day_of_week, counter)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    # Execute the CQL statement with the event data
    session.execute(cql, (event_data['member_name'], created_at, event_data['check_in_time'], event_data.get('check_out_time', None), event_data['day_of_week'], event_data['counter']))
    print(f"DEBUG -- Inserted/Updated {event_data['member_name']}'s gym alert data.")

try:
    print("Starting Cassandra log consumer…")
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                continue
            else:
                print(msg.error())
                break

        # Deserialize the event data
        event_data = json.loads(msg.value().decode('utf-8'))

        if 'member_id' not in event_data:
            print("Skipping event without member_id:", event_data)
            continue
        
        # Insert into Cassandra
        if event_data['counter'] > 10:
            project_into_cassandra(event_data)
            print(f"DEBUG -- DB Alert Projection Service: Inserted event for member {event_data['member_name']} into Cassandra... Gym approaching maximum capacity..")
except KeyboardInterrupt:
    pass
finally:
    # Clean up on exit
    consumer.close()
    cassandra_cluster.shutdown()
