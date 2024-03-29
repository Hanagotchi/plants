# Plants Microservice

This is a microservice that provides information about plants.

## Documentation

- Swagger documentation: `http://localhost:PORT/docs`.
- ReDoc documentation: `http://localhost:PORT/redoc`.

Where `PORT` is the port where the microservice is running defined in the [env](.env) file.

## Environment Variables

Environment variables are defined in the [env.example](.env.example) file.

## README

## Environment Variables

### Application Configuration
- `PORT`: The port number on which the application will run. Example value: `8081`.
- `LOGGING_LEVEL`: The logging level for the application. Example values: `DEBUG`, `INFO`.

### PostgreSQL Database Connection
- `POSTGRES_USER`: The username to connect to the PostgreSQL database. Example value: `user`.
- `POSTGRES_PASSWORD`: The password to connect to the PostgreSQL database. Example value: `1234`.
- `POSTGRES_DB`: The name of the database containing the data. Example value: `dev`. 
- `POSTGRES_HOST`: The hostname or IP address of the PostgreSQL server. Example value: `sql`.
- `POSTGRES_PORT`: The port number of the PostgreSQL server. Example value: `5432`.
- `POSTGRES_SCHEMA`: The name of the schema within the database where relevant tables are located. Example value: `plants_service`.
- `DATABASE_URL`: The URL for connecting to the PostgreSQL database in the format `postgres://<username>:<password>@<host>:<port>/<database>`. Example value: `postgres://user:1234@sql:5432/dev`.

### External Services
- `MEASUREMENTS_SERVICE_URL`: The URL for communicating with the measurements microservice. Example value: `http://measurements:8080`.
- `USERS_SERVICE_URL`: The URL for communicating with the users microservice. Example value: `http://users:8082`. 


## Poetry

This project uses [Poetry](https://python-poetry.org/) to manage dependencies.

### Install Poetry

```$ pip install poetry```

### Install dependencies

```$ poetry install```

### Add new dependency

```$ poetry add <dependency>```

### Update dependencies

```$ poetry update```

### Poetry locks

After any change in pyproject.toml file (always execute this before installing):

```$ poetry lock```

## Docker

#### Build container

```$ docker-compose build```

#### Start services

```$ docker-compose up```

#### List images

```$ docker images```

#### Remove dangling images: 

When you run a docker-compose build, it creates a new image, but it doesn't remove the old one, so you can have a lot of images with the same name but different id. Then, you can remove all of them with the following command:

```$ docker rmi $(docker images -f dangling=true -q) -f```

#### Deep Cleaning - Free space on your disk
*Warning*: This will remove all containers, images, volumes and networks not used by at least one container.
Its *recommended* to run this command before docker-compose up to avoid problems.

```$ docker system prune -a --volumes```

#### Usage Instructions with Makefile
The repository includes a **Makefile** that encapsulates various commands used frequently in the project as targets. The targets are executed by invoking:

* **make \<target\>**:
The essential targets to start and stop the system are **docker-compose-up** and **docker-compose-down**, with the remaining targets being useful for debugging and troubleshooting.

Available targets are:
* **docker-compose-up**: Initializes the development environment (builds docker images for the server and client, initializes the network used by docker, etc.) and starts the containers of the applications that make up the project.
* **docker-compose-down**: Performs a `docker-compose stop` to stop the containers associated with the compose and then performs a `docker-compose down` to destroy all resources associated with the initialized project. It is recommended to execute this command at the end of each run to prevent the host machine's disk from filling up.
* **docker-compose-logs**: Allows viewing the current logs of the project. Use with `grep` to filter messages from a specific application within the compose.
* **docker-image**: Builds the images to be used. This target is used by **docker-compose-up**, so it can be used to test new changes in the images before starting the project.

