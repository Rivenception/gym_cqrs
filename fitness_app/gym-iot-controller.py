#pip install mysql-connector-python confluent_kafka
#pip install mysql-connector-python

#you might need to reset to the older password style for this to work:
#ALTER USER 'root'@'localhost'
#IDENTIFIED WITH mysql_native_password BY 'your_password';

import json
from confluent_kafka import Producer
import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime
import time
import creds
from collections import defaultdict

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))

def buildConnection():
    connection = mysql.connector.connect(
    host= creds.db_host,
    database= creds.db_database,
    user= creds.db_user,
    password= creds.db_password
    )
    return connection

# active_members = {}

def collect_gym_data(active_members, daily_capacity):
    try:
        # Kafka configuration
        conf = {
            'bootstrap.servers': "localhost:9093",  # Change this to your Kafka server configuration
        }
        # Create Producer instance
        producer = Producer(**conf)
        # Connect to the MySQL database
        connection = buildConnection()
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)

            cursor = connection.cursor()

            members = [
                "Alice", "Bob", "Charlie", "Diana", "Evan",
                "Fiona", "George", "Hannah", "Isaac", "Jasmine",
                "Kevin", "Luna", "Miles", "Nina", "Oscar",
                "Paula", "Quinn", "Ryan", "Sophie", "Tyler",
                "Uma", "Victor", "Wendy", "Xander", "Yara",
                "Zane", "Liam", "Noah", "Olivia", "Zoe"
            ]
                
            member_name = random.choice(members)

            hours = random.randint(6, 23)
            minutes = random.randint(0, 59)
            check_in_time = f"{hours:02d}:{minutes:02d}"
            day_of_week = random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
            count = 0

            ## implement using dictionaries instead of lists
            if member_name not in active_members:
                
                check_out_time = None
                # count = len(active_members)
                daily_capacity[day_of_week] += 1
                count = daily_capacity[day_of_week]

                # Insert command
                insert_query = """
                    INSERT INTO gym_alerts (member_name, check_in_time, check_out_time, day_of_week, counter)
                    VALUES (%s, %s, %s, %s, %s)
                    """

                record = (member_name, check_in_time, check_out_time, day_of_week, count)
                cursor.execute(insert_query, record)
                connection.commit()

                print(f"DEBUG -- {member_name} has entered the gym at {check_in_time} on {day_of_week}.")
                row_id = cursor.lastrowid

                active_members[member_name] = {
                    'check_in_time': check_in_time,
                    'day_of_week': day_of_week,
                    'row_id': row_id
                }
            else:
                # Record check-out time and remove member from active_members
                info = active_members.pop(member_name)
                check_in_time = info['check_in_time']
                day_of_week = info['day_of_week']
                row_id = info['row_id']
                hours, minutes = map(int, check_in_time.split(':'))
                # Increment the hour for check-out time
                minutes = (minutes + random.randint(1, 30)) % 60
                hours = (hours + 1) % 24
                # Format check-out time
                check_out_time = f"{hours:02d}:{minutes:02d}"
                # Update the count of active members
                count = len(active_members)
                print(f"DEBUG -- {member_name} has left the gym at {check_out_time} on {day_of_week}.")

                update_query = """
                    UPDATE gym_alerts
                    SET check_out_time = %s, counter = %s
                    WHERE id = %s
                """
                cursor.execute(update_query, (check_out_time, count, row_id))
                connection.commit()

            cursor.execute("SELECT member_id FROM gym_members WHERE member_name=%s", (member_name,))
            member_id = cursor.fetchone()[0]    


            gym_status_event = {
                'member_id': member_id,
                'member_name': member_name,
                'check_in_time': check_in_time,
                'check_out_time': check_out_time,
                'day_of_week': day_of_week,
                'counter': count,
            }
            event_json = json.dumps(gym_status_event) # serialize the data to an event.
            connection.commit()
            producer.produce("gym", event_json.encode('utf-8'), callback=acked)

            # Wait for any outstanding messages to be delivered
            producer.flush()

            print("Event pushed to topic 'gym'.")
            print(f"New log inserted: Member Name: {member_name}, Check In: {check_in_time}, Check Out: {check_out_time}, On: {day_of_week}"
)

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def main():
    active_members = {}
    daily_capacity = defaultdict(int)
    while True:
        collect_gym_data(active_members, daily_capacity)
        time.sleep(5)  # Pause for 1 second before the next insert

if __name__ == '__main__':
    main()
