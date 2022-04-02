import json
import pytest
from app.database.connector import engine, Base
from app.main import app
from fastapi.testclient import TestClient
from app.core.config import get_app_settings

SETTINGS = get_app_settings()


def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def create_admin():
    client = TestClient(app)
    data = {
        "username": SETTINGS.test_admin_user,
        "hashed_password": SETTINGS.test_admin_password,
        "email": f"{SETTINGS.test_admin_user}@gmail.com",
        "full_name": f"{SETTINGS.test_admin_user.replace('_', ' ').title()}",
    }
    response = client.post("/users/create", json.dumps(data))
    return response


def create_users():
    client = TestClient(app)
    for i in range(10):
        data = {
            "username": f"user_{i}",
            "hashed_password": f"string_{i}",
            "email": f"user.{i}@gmail.com",
            "full_name": f"user_{i}".replace("_", " ").title(),
        }
        response = client.post("/users/create", json.dumps(data))
        if response.status_code != 200:
            raise Exception("Unable to create user")


@pytest.fixture()
def admin_token(client):
    data = {
        "grant_type": "password",
        "username": SETTINGS.test_admin_user,
        "password": SETTINGS.test_admin_password,
    }
    response = client.post(
        "/auth/token",
        data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return response.json()["access_token"]


@pytest.fixture()
def user_token(client):
    data = {
        "grant_type": "password",
        "username": "user_1",
        "password": "string_1",
    }
    response = client.post(
        "/auth/token",
        data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return response.json()["access_token"]


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def db_initial_state():
    setup_db()
    create_admin()
    create_users()


setup_db()
create_admin()
create_users()
