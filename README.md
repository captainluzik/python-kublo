# python-kublo
Python/Django Кубло


## Prerequisites
Before you begin, ensure you have met the following requirements:
- You have [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed on your machine.

Make sure to set the required environment variables in the .env file before running the project. 
Refer to the .env.example file for a template of the required variables.

## Start 
To start the project, run the following command
```docker
docker-compose up --build --abort-on-container-exit
```
- The `--build` flag ensures that the images are built before starting the containers.
- The `--abort-on-container-exit` flag stops all containers if any container exits with
a non-zero status (used to make sure that all tests are passed).

Also, you can run the project using at your own risk and if you are sure that possible incorrectly passed tests will not affect the performance of the program
```docker
docker-compose up -d --build
```
- The `-d` flag used to run docker in detached mode so you can use your terminal
- The `--build` flag ensures that the images are built before starting the containers.


## Accessing the Application
Once the containers are up and running, you can access the application in your web browser at http://localhost:8000
(or the appropriate port if you've configured it differently).

## Stopping the Project
To stop the project and containers, press Ctrl+C in the terminal
or run `docker-compose down`(if you've run project with `docker-compose up -d --build` command) where docker-compose is running. This will gracefully shut down the containers.
