import json
from app.core.config import get_app_settings

SETTINGS = get_app_settings()


def test_create_placelist(client, admin_token, create_placelists):
    response = client.post(
        "/placelists/",
        params={"placelist_name": "a placelist"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200


def test_get_placelist(client, admin_token, create_placelists):
    response = client.get(
        "/placelists/",
        params={"placelist_id": 1},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200


def test_update_placelist(client, admin_token, create_placelists):
    response = client.put(
        "/placelists/",
        data=json.dumps({"id": 2, "name": "an updated placelist"}),
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    assert response["name"] == "an updated placelist"
    assert len(response["updated_date"]) == 26


def test_get_placelists(client, admin_token, create_placelists):
    response = client.get(
        "/placelists/all",
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    assert len(response) == 4


def test_append_remove_from_placelist(
    client, admin_token, create_placelists, create_places
):
    append_response = client.post(
        "/placelists/append",
        params={"place_id": 1, "placelist_id": 1},
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    remove_response = client.post(
        "/placelists/remove",
        params={"place_id": 1, "placelist_id": 1},
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    assert len(append_response["places"]) == 1
    assert len(remove_response["places"]) == 0


def test_append_two_placelist(
    client, admin_token, create_placelists, create_places, populate_placelists
):
    attached_response = client.get(
        "/places/",
        params={"place_id": 5},
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    assert len(attached_response["placelists"]) == 2


def test_delete_placelist(
    client, admin_token, create_placelists, create_places, populate_placelists
):
    client.delete(
        "/placelists/",
        params={"placelist_id": 3},
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    attached_response = client.get(
        "/places/",
        params={"place_id": 5},
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    assert len(attached_response["placelists"]) == 1
