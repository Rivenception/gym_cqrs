import time
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
#https://cassandra.apache.org/_/quickstart.html
def main():
    # Configure the connection:
    cassandra_cluster = Cluster(['127.0.0.1'], port=9042)

    # Connect to the cluster:
    try:
        # session = cassandra_cluster.connect()
        session = cassandra_cluster.connect('fitness_app')
        print("Connected to Cassandra cluster.")

        rows = session.execute("SELECT day_of_week, counter FROM fitness_app.gym_alerts;")

                    # Aggregate data
        stats = {}
        for row in rows:
            day = row.day_of_week
            count = row.counter

            if day not in stats:
                stats[day] = {'total': 0, 'entries': 0}

            stats[day]['total'] += count
            stats[day]['entries'] += 1

        # Display average capacity per day
        print("\n--- Average Gym Capacity by Day of Week ---")
        for day, data in stats.items():
            avg = data['total'] / data['entries'] if data['entries'] > 0 else 0
            print(f"{day}: {avg:.2f} active members")

    except Exception as e:
        print("Failed to connect to Cassandra cluster:", e)
    finally:
        cassandra_cluster.shutdown()

if __name__ == "__main__":
    main()