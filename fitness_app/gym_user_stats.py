import time
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from datetime import datetime
#https://cassandra.apache.org/_/quickstart.html

def parse_time_str(t):
    """Parse HH:MM string into datetime object for calculation."""
    return datetime.strptime(t, '%H:%M')

def compute_duration(start, end):
    """Return workout duration in minutes."""
    delta = parse_time_str(end) - parse_time_str(start)
    return delta.total_seconds() / 60 if delta.total_seconds() > 0 else 0

def main():
    # Configure the connection:
    cassandra_cluster = Cluster(['127.0.0.1'], port=9042)

    # Connect to the cluster:
    try:
        # session = cassandra_cluster.connect()
        session = cassandra_cluster.connect('fitness_app')
        print("Connected to Cassandra cluster.")


        query = """
            SELECT member_name, day_of_week, check_in_time, check_out_time 
            FROM gym_alerts 
            ALLOW FILTERING;
        """
        rows = session.execute(query)

        stats = {}

        for row in rows:
            if not row.check_in_time or not row.check_out_time:
                continue  # Skip incomplete rows

            member = row.member_name
            day = row.day_of_week
            in_time = row.check_in_time
            out_time = row.check_out_time

            if not (in_time and out_time):
                continue  # Skip if either time is missing

            duration = compute_duration(in_time, out_time)

            key = (member, day)
            if key not in stats:
                stats[key] = {'visits': 0, 'total_duration': 0}

            stats[key]['visits'] += 1
            stats[key]['total_duration'] += duration

        print("\n--- Member Weekly Visit Stats ---")
        for (member, day), data in stats.items():
            avg_duration = data['total_duration'] / data['visits']
            print(f"{member} - {day}: {data['visits']} visits, avg duration: {avg_duration:.1f} minutes")

        # for row in rows:
        #     print(f'{row.day_of_week} has entered the gym. Gym capacity is at {row.counter}')
        # time.sleep(10)
    except Exception as e:
        print("Failed to connect to Cassandra cluster:", e)
    finally:
        cassandra_cluster.shutdown()

if __name__ == "__main__":
    main()