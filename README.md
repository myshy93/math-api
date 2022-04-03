# Math Microservice

Simple math operations done in a microservice.

Tech stack:

- FastAPI
- Uvicorn
- FastAPI Cache with memcache
- AioKafka

## Install requirements

```shell
pip -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Configurable environment settings

| Variable name               | Description          | Default                      |
|-----------------------------|----------------------|------------------------------|
| API_V1_STR                  | API V1 prefix        | /api/v1                      |
| SECRET_KEY                  | Secret key for JWT   | Randon generated             |
| ACCESS_TOKEN_EXPIRE_MINUTES | JWT Expire minutes   | 11520 (8 days)               |
| PROJECT_NAME                | Project name         | Math Microservice            |
| DEBUG                       | Enable debugging     | False                        |
| DATABASE_URL                | Database URL         | sqlite:///./db-files/math.db |
| SERVER_URL                  | Trusted hostname     | localhost                    |
| SENTRY_DSN                  | Sentry DSN           | None                         |
| KAFKA_SERVER                | Kafka broker address | localhost                    |
| KAFKA_PORT                  | Kafka broker port    | 9092                         |

NOTE: When DEBUG is True logging verbosity will increase and default users will be created.

NOTE: In DEBUG mode all hosts will be treated as trusted.

## Run the server for development

```shell
python -m uvicorn app.main:app --reload
```

## Deploy with docker

1. Copy .env.sample and rename it .env. Here you will place all configuration variables.
   ```shell
    cp .env.sample .env
    ```

2. Run docker compose
   ```shell
   cd kafka
   docker-compose up -d
   cd ..
   docker-compose up -d
   ```

3. [Optional] Rebuild image
    ```shell
   docker-compose up -d --build
    ```

## How to use

### Default user/password

```shell
email: test@test.com
password: test
```

### Read events from Kafka

```shell
docker exec --interactive --tty broker \
kafka-console-consumer --bootstrap-server broker:9092 \
                       --topic quickstart \
                       --from-beginning
```

## Known issues

1. ELK stack is not stable and needs configuration adjustments.
2. Documentation UI will return null (as represented result) for large int numbers returnerd by endpoints.