

def test_basic(test_client):
    response = test_client.get("/oai")
    assert response.status_code == 200