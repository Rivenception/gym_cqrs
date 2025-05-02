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