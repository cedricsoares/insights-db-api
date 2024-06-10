from datetime import datetime


def test_get_existing_page(mocker, db_connection, client):
    mocker.patch("sqlite3.connect", return_value=db_connection)

    resp = client.get("/page/1")

    assert resp.status_code == 200

    data = resp.get_json()

    assert data["code"] == 0
    assert data["message"] == "ok"
    assert data["data"]["id"] == 1
    assert data["data"]["name"] == "fake_name"

    created_at = data["data"]["created_at"]

    if created_at:
        try:
            datetime.fromisoformat(created_at)
        except ValueError:
            assert (
                False
            ), f"Expected created_at to be a valid ISO date, but got {created_at}"


def test_get_non_existing_page(mocker, db_connection, client):
    mocker.patch("sqlite3.connect", return_value=db_connection)

    resp = client.get("/page/999")

    assert resp.status_code == 404

    data = resp.get_json()

    assert data["code"] == -1
    assert data["message"] == "Resource not found!"


def test_add_page(client, db_connection):
    data = {"id": 1111, "name": "new page name"}
    response = client.post("/page", json=data)
    assert response.status_code == 200
    assert response.json["data"]["name"] == "new page name"


def test_add_page_missing_name(client, db_connection):
    data = {"id": 2, "created_at": "2023-01-01T00:00:00"}
    response = client.post("/page", json=data)
    assert response.status_code == 422


def test_add_page_invalid_date_format(client, db_connection):
    data = {
        "name": "New Page Name",
        "created_at": "2023-01-01",  # Invalid date format
    }
    response = client.post("/page", json=data)
    assert response.status_code == 422
