# Math Microservice

Simple math operations done in a microservice.

Tech stack:

- FastAPI
- Uvicorn
- FastAPI Cache with memcache

## Install requirements

```shell
pip -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Configurable environment settings

| Variable name                | Description        | Default           |
|------------------------------|--------------------|-------------------|
| API_V1_STR                   | API V1 prefix      | /api/v1           |
| SECRET_KEY                   | Secret key for JWT | Randon generated  |
| ACCESS_TOKEN_EXPIRE_MINUTES  | JWT Expire minutes | 11520 (8 days)    |
| PROJECT_NAME                 | Project name       | Math Microservice |

## Run the server

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
   docker-compose up -d
   ```
   
3. [Optional] Rebuild image
    ```shell
   docker-compose up -d --build
    ```