from datetime import datetime


def test_get_existing_page(mocker, db_connection, client):
    mocker.patch("sqlite3.connect", return_value=db_connection)

    resp = client.get("/page/1")

    assert (
        resp.status_code == 200
    ), f"Expected status code 200, but got {resp.status_code}"

    data = resp.get_json()

    assert data["code"] == 0, f"Expected code 0, but got {data['code']}"
    assert data["message"] == "ok", f"Expected message 'ok', but got {data['message']}"
    assert data["data"]["id"] == 1, f"Expected id 1, but got {data['data']['id']}"
    assert (
        data["data"]["name"] == "fake_name"
    ), f"Expected name 'fake_name', but got {data['data']['name']}"

    created_at = data["data"]["created_at"]
    if created_at:
        try:
            datetime.fromisoformat(created_at)
        except ValueError:
            assert (
                False
            ), f"Expected created_at to be a valid ISO date, but got {created_at}"


def test_get_non_existing_page(mocker, db_connection, client):
    # Corrigez la faute de frappe ici
    mocker.patch("sqlite3.connect", return_value=db_connection)

    # Faites une requête GET à l'endpoint /page/999 (en supposant que cette page n'existe pas)
    resp = client.get("/page/999")

    # Vérifiez que le statut de la réponse est 404
    assert (
        resp.status_code == 404
    ), f"Expected status code 404, but got {resp.status_code}"

    # Vérifiez le contenu de la réponse
    data = resp.get_json()

    assert data["code"] == -1, f"Expected code -1, but got {data['code']}"
    assert (
        data["message"] == "Resource not found!"
    ), f"Expected message 'Resource not found!', but got {data['message']}"
