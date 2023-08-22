# python-kublo
Python/Django Кубло

### Prerequisites

What you need to run project
- Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) on your machine.
- Create and fill `.env` file using `.env.example` as template

### How to run project
There are two ways to run project.
#### 1. Simply run all containers
```docker-compose up -d --build```

This command will start all containers, but be careful, if tests fail, django app won't start!

Flags:

- `-d` used to run containers in detached mode
- `--build` used to build images before containers start

#### 2. Run and stop on tests fail
```docker-compose up --build --abort-on-container-exit```

In this way, if tests fail, build will fail as well.

Flags:

- `--abort-on-container-exit` will stop build if some container exits

### How to stop project

If your container is attached to current terminal session, press `CTRL + C`.

In detached mode, run `docker-compose down`
