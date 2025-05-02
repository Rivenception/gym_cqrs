from collections import defaultdict, Counter
from cassandra.cluster import Cluster

def main():
    cassandra_cluster = Cluster(['127.0.0.1'], port=9042)

    try:
        session = cassandra_cluster.connect('fitness_app')
        print("Connected to Cassandra cluster.")

        # Fetch check-in times and day of week
        rows = session.execute("SELECT day_of_week, check_in_time FROM fitness_app.gym_alerts;")

        # Structure to store hourly frequency per day
        hourly_counts = defaultdict(Counter)

        for row in rows:
            day = row.day_of_week
            hour = int(row.check_in_time.split(":")[0])  # Extract hour from "HH:MM"
            hourly_counts[day][hour] += 1

        print("\n🏋️" + " Peak Hours by Day of Week 🕒")
        for day, hour_counter in hourly_counts.items():
            peak_hour, visits = hour_counter.most_common(1)[0]
            print(f"{day}: {peak_hour:02d}:00 with {visits} check-ins")

    except Exception as e:
        print("Failed to connect to Cassandra cluster:", e)
    finally:
        cassandra_cluster.shutdown()

if __name__ == "__main__":
    main()
