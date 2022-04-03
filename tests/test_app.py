from fastapi.testclient import TestClient
import os

from app.db.init_db import init_db
from app.main import app
from app.core.config import default_user, settings

client = TestClient(app)

init_db()

os.environ.setdefault("DEBUG", "True")


def test_root():
    response = client.get("/")
    assert response.status_code == 404


def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200


def test_token_auth():
    response = client.post(
        "/token",
        data={
            "username": default_user["email"],
            "password": default_user["password"]
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    return response.json()['access_token']


def test_pow():
    response = client.get(f"{settings.API_V1_STR}/math/pow?base=2&exp=2")
    assert response.status_code == 200
    assert response.json()['result'] == 4


def test_pow_overflow():
    response = client.get(f"{settings.API_V1_STR}/math/pow?base=20000&exp=200000")
    assert response.status_code == 409


def test_pow_invalid():
    response = client.get(f"{settings.API_V1_STR}/math/pow?base=alfa&exp=unu")
    assert response.status_code == 422
    response = client.get(f"{settings.API_V1_STR}/math/pow?base=12")
    assert response.status_code == 422


def test_n_th_fibonacci():
    response = client.get(f"{settings.API_V1_STR}/math/fibonacci?n=8")
    assert response.status_code == 200
    assert response.json()['result'] == 13


def test_n_th_fibonacci_invalid():
    response = client.get(f"{settings.API_V1_STR}/math/fibonacci?n=-10")
    assert response.status_code == 422
    response = client.get(f"{settings.API_V1_STR}/math/fibonacci?n=aaa")
    assert response.status_code == 422


def test_factorial_guest():
    response = client.get(f"{settings.API_V1_STR}/math/factorial")
    assert response.status_code == 401


def test_factorial_invalid_auth():
    token = test_token_auth()
    response = client.get(f"{settings.API_V1_STR}/math/factorial", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 422
    response = client.get(f"{settings.API_V1_STR}/math/factorial?n=-3", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 422


def test_factorial_valid_auth():
    token = test_token_auth()
    response = client.get(f"{settings.API_V1_STR}/math/factorial?n=4", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json()['result'] == 24
