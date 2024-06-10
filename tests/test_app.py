from datetime import datetime
import pytest


@pytest.mark.skip(reason="The test is not workink yet")
def test_get_existing_page(mocker, db_connection, client):
    mocker.patch("sqlite3.connect", return_value=db_connection)

    resp = client.get("/page/11")

    assert resp.status_code == 200

    data = resp.get_json()

    assert data["code"] == 0
    assert data["message"] == "ok"
    assert data["data"]["id"] == 11
    assert data["data"]["name"] == "fake_name"

    created_at = data["data"]["created_at"]

    if created_at:
        try:
            datetime.fromisoformat(created_at)
        except ValueError:
            assert (
                False
            ), f"Expected created_at to be a valid ISO date, but got {created_at}"


@pytest.mark.skip(reason="The test is not workink yet")
def test_get_non_existing_page(mocker, db_connection, client):
    mocker.patch("sqlite3.connect", return_value=db_connection)

    resp = client.get("/page/999")

    assert resp.status_code == 404

    data = resp.get_json()

    assert data["code"] == -1
    assert data["message"] == "Resource not found!"


@pytest.mark.skip(reason="The test is not workink yet")
def test_add_page(client, db_connection):
    data = {"id": 769112, "name": "new page name"}
    response = client.post("/page", json=data)
    assert response.status_code == 200
    assert response.json["data"]["name"] == "new page name"


@pytest.mark.skip(reason="The test is not workink yet")
def test_add_page_missing_name(client, db_connection):
    data = {"id": 2, "created_at": "2023-01-01T00:00:00"}
    response = client.post("/page", json=data)
    assert response.status_code == 422


@pytest.mark.skip(reason="The test is not workink yet")
def test_delete_existing_page(mocker, db_connection, client):
    mocker.patch("sqlite3.connect", return_value=db_connection)

    client.post("/page", json={"id": 222, "name": "page_to_delete"})

    resp = client.delete("/page/222")

    db_connection.commit()

    assert resp.status_code == 200


@pytest.mark.skip(reason="The test is not workink yet")
def test_get_existing_video(mocker, db_connection, client):
    mocker.patch("sqlite3.connect", return_value=db_connection)

    resp = client.get("/video/11")

    assert resp.status_code == 200

    data = resp.get_json()

    assert data["code"] == 0
    assert data["message"] == "ok"
    assert data["data"]["id"] == 11
    assert data["data"]["page_id"] == 11
    assert data["data"]["title"] == "fake_title"


@pytest.mark.skip(reason="The test is not workink yet")
def test_get_non_existing_video(mocker, db_connection, client):
    mocker.patch("sqlite3.connect", return_value=db_connection)

    resp = client.get("/video/999")

    assert resp.status_code == 404

    data = resp.get_json()

    assert data["code"] == -1
    assert data["message"] == "Resource not found!"


@pytest.mark.skip(reason="The test is not workink yet")
def test_add_video(client, db_connection):
    data = {"id": 5559, "page_id": 1, "title": "new video title"}
    response = client.post("/video", json=data)
    assert response.status_code == 200
    assert response.json["data"]["title"] == "new video title"


def test_add_video_missing_title(client, db_connection):
    data = {"id": 2, "page_id": 1}
    response = client.post("/video", json=data)
    assert response.status_code == 422


@pytest.mark.skip(reason="The test is not workink yet")
def test_delete_existing_video(mocker, db_connection, client):
    mocker.patch("sqlite3.connect", return_value=db_connection)

    client.post("/video", json={"id": 333, "page_id": 1, "title": "video_to_delete"})

    resp = client.delete("/video/333")

    db_connection.commit()

    assert resp.status_code == 200


@pytest.mark.skip(reason="The test is not workink yet")
def test_get_existing_video_insight(mocker, db_connection, client):
    mocker.patch("sqlite3.connect", return_value=db_connection)

    resp = client.get("/video_insight/1")

    assert resp.status_code == 200

    data = resp.get_json()

    assert data["code"] == 0
    assert data["message"] == "ok"
    assert data["data"]["id"] == 11
    assert data["data"]["video_id"] == 11
    assert data["data"]["likes"] == 11
    assert data["data"]["views"] == 11

    created_at = data["data"]["created_at"]

    if created_at:
        try:
            datetime.fromisoformat(created_at)
        except ValueError:
            assert (
                False
            ), f"Expected created_at to be a valid ISO date, but got {created_at}"


@pytest.mark.skip(reason="The test is not workink yet")
def test_get_non_existing_video_insight(mocker, db_connection, client):
    mocker.patch("sqlite3.connect", return_value=db_connection)

    resp = client.get("/video_insight/999")

    assert resp.status_code == 404

    data = resp.get_json()

    assert data["code"] == -1
    assert data["message"] == "Resource not found!"


@pytest.mark.skip(reason="The test is not workink yet")
def test_add_video_insight(client, db_connection):
    data = {"id": 557, "video_id": 1, "likes": 5, "views": 50}
    response = client.post("/video_insight", json=data)
    assert response.status_code == 200
    assert response.json["data"]["likes"] == 5
    assert response.json["data"]["views"] == 50


@pytest.mark.skip(reason="The test is not workink yet")
def test_add_video_insight_missing_fields(client, db_connection):
    data = {"id": 2}
    response = client.post("/video_insight", json=data)
    assert response.status_code == 422


@pytest.mark.skip(reason="The test is not workink yet")
def test_delete_existing_video_insight(mocker, db_connection, client):
    mocker.patch("sqlite3.connect", return_value=db_connection)

    client.post(
        "/video_insight", json={"id": 333, "video_id": 1, "likes": 5, "views": 50}
    )

    resp = client.delete("/video_insight/333")

    db_connection.commit()

    assert resp.status_code == 200
