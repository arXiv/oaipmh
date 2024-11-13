from oaipmh.data.oai_properties import OAIParams, OAIVerbs

def test_good_params(test_client):
    #general case
    params = {OAIParams.VERB: OAIVerbs.LIST_META_FORMATS}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" not in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" not in text

    #for an item
    params = {OAIParams.VERB: OAIVerbs.LIST_META_FORMATS, OAIParams.ID : "item"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" not in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" not in text

def test_extra_params(test_client):
    #general case
    params = {OAIParams.VERB: OAIVerbs.LIST_META_FORMATS, OAIParams.FROM:"now"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" in text
    assert "Only allowed parameters are" in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" in text
    assert "Only allowed parameters are" in text

    #with an id
    params = {OAIParams.VERB: OAIVerbs.LIST_META_FORMATS, OAIParams.ID:"something", OAIParams.FROM:"now"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" in text
    assert f"Only {OAIParams.ID} parameter allowed" in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" in text
    assert f"Only {OAIParams.ID} parameter allowed" in text