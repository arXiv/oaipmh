

def test_good_params(test_client):
    params = {"verb": "Identify"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" not in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" not in text

def test_extra_params(test_client):
    params = {"verb": "Identify", "identifier": "oai:example.org:record123"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" in text