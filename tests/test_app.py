def test_request_example(client):
    res = client.get("/")
    assert res.status_code == 200
