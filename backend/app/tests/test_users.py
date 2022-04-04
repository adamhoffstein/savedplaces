import json
from app.core.config import get_app_settings

SETTINGS = get_app_settings()


def test_admin_login(client):
    data = {
        "grant_type": "password",
        "username": SETTINGS.test_admin_user,
        "password": SETTINGS.test_admin_password,
    }
    response = client.post("/auth/token", data)
    assert response.status_code == 200


def test_user_login(client):
    data = {
        "grant_type": "password",
        "username": "user_1",
        "password": "string_1",
    }
    response = client.post("/auth/token", data)
    assert response.status_code == 200


def test_admin_login_wrong_password(client):
    data = {
        "grant_type": "password",
        "username": SETTINGS.test_admin_user,
        "password": "wrongpassword",
    }
    response = client.post("/auth/token", data)
    assert response.status_code == 401


def test_admin_is_admin(client, admin_token):
    response = client.get(
        "/users/",
        params={"user_id": 1},
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    assert response["username"] == "test_admin"
    assert response["super_admin"] == True


def test_update_user(client, admin_token):
    response = client.put(
        "/users/",
        data=json.dumps(
            {
                "id": 1,
                "email": "a@newemail.com",
                "full_name": "a new name",
            }
        ),
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    assert response["full_name"] == "a new name"
    assert response["email"] == "a@newemail.com"


def test_get_all_users(client, admin_token):
    response = client.get(
        "/users/all", headers={"Authorization": f"Bearer {admin_token}"}
    ).json()
    assert len(response) == 11


def test_create_user(client):
    data = {
        "username": "newuser",
        "hashed_password": "12345",
        "email": "user@gmail.com",
        "full_name": "User Name",
    }
    response = client.post("/users/", json.dumps(data))
    assert response.status_code == 200
