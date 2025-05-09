# gym_cqrs
CSC 545 final project


# Instructions after cloning repo
- run docker-compose up -d in terminal where the docker-compose.yaml file location is stored
- pip install missing dependencies as needed
- create a creds.py folder and .gitignore file in the same directory location
    - in .gitignore add your creds.py file to the list
    - in creds.py add the below
        - db_host = 'your ip address'
        - bd_database = 'your database'
        - db_user = 'root' or 'your user_id"
        - db_password = 'your password'

# To access cqlsh
- open cmd
- type in docker ps to pull the list of docker containers
- type in docker exec -it "cassandra container name" cqlsh
- USE fitness_app; to access the tables

# Initial Idea

I’d like to design a gym check-in system with the goal of helping fitness centers track and analyze member activity with a flexible, event-driven setup. The application focuses on the simplest component of gym operations – membership and attendance. Most gyms have a member checking in and out, and it is this data that I would like to use to generate useful workout insights. The system would be designed for gym admins, who can track things like peak hours and member streaks; gym members, who can see their own stats, like total time spent at the gym and their longest streak; and data analysts, who can use the data to improve business operations. The build would likely be a command line system for the requirements of this project.