import json
from app.core.config import get_app_settings

SETTINGS = get_app_settings()


def test_create_place(client, admin_token, create_places):
    data = {"google_place_id": "an_id", "name": "a place"}
    response = client.post(
        "/places/",
        json.dumps(data),
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200


def test_get_place(client, admin_token, create_places):
    response = client.get(
        "/places/",
        params={"place_id": 1},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200


def test_delete_place(client, admin_token, create_places):
    response = client.delete(
        "/places/",
        params={"place_id": 1},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200


def test_get_all_places(client, admin_token, create_places):
    response = client.get(
        "/places/all",
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    assert len(response) == 9


def test_update_place(client, admin_token, create_places):
    data = {"id": 2, "name": "a different place"}
    response = client.put(
        "/places/",
        json.dumps(data),
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    assert response["name"] == "a different place"
    assert len(response["updated_date"]) == 26
