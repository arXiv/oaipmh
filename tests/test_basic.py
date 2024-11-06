

def test_basic(test_client):
    response = test_client.get("/oai")
    text=response.text
    assert response.status_code == 200
    assert 'xmlns="http://www.openarchives.org/OAI/2.0/"' in text
    assert '<responseDate>' in text
    assert '/oai</request>' in text