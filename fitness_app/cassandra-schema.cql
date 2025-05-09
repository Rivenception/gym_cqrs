
#docker exec -it my-cassandra cqlsh

#fitness_app schema

CREATE KEYSPACE IF NOT EXISTS fitness_app
WITH replication = {
    'class': 'SimpleStrategy', 
    'replication_factor': 1  -- Adjust based on your cluster setup
};

USE fitness_app;

CREATE TABLE IF NOT EXISTS gym_members (
    member_id int,
    created_at timestamp,
    member_name text,
    PRIMARY KEY ((member_id), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);

CREATE TABLE IF NOT EXISTS gym_tracker (
    member_id int,
    created_at timestamp,
    member_name text,
    check_in_time text,
    check_out_time text,
    day_of_week text,
    PRIMARY KEY ((member_id), created_at)
) WITH CLUSTERING ORDER BY (created_at DESC);

CREATE TABLE IF NOT EXISTS gym_alerts (
    member_name text,
    day_of_week text,
    check_in_time text,
    check_out_time text,
    counter int,
    created_at timestamp,
    PRIMARY KEY ((member_name), created_at)
) WITH CLUSTERING ORDER BY (created_at DESC);

// for tracking who is currently at the gym
CREATE TABLE IF NOT EXISTS gym_active_members (
    member_id int PRIMARY KEY,
    member_name text,
    check_in_time time,
    day_of_week text
);

// for tracking daily summaries (number of visits or peak times)
CREATE TABLE IF NOT EXISTS gym_day_stats (
    day_of_week text,
    date text,
    total_check_ins int,
    peak_time time,
    PRIMARY KEY ((day_of_week), date)
);
