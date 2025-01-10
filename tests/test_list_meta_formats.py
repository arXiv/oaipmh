from oaipmh.data.oai_properties import OAIParams, OAIVerbs

def test_good_params(test_client):
    #general case
    params = {OAIParams.VERB: OAIVerbs.LIST_META_FORMATS}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" not in text
    assert '<metadataPrefix>arXiv</metadataPrefix>' in text
    assert '<metadataNamespace>http://www.openarchives.org/OAI/2.0/oai_dc/</metadataNamespace>' in text
    assert '<schema>http://arxiv.org/OAI/arXivRaw.xsd</schema>' in text
    assert '<ListMetadataFormats>' in text
    assert '<request verb="ListMetadataFormats">' in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    assert response.headers["Content-Type"] == "application/xml"
    assert response.headers["Surrogate-Control"] == "max-age=31536000"
    assert response.headers["Surrogate-Key"] == "oai"
    text=response.get_data(as_text=True)
    assert "<error code=" not in text

    #for an item
    params = {OAIParams.VERB: OAIVerbs.LIST_META_FORMATS, OAIParams.ID : "oai:arXiv.org:1001.3172"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" not in text
    assert "<error code=" not in text
    assert '<metadataPrefix>arXiv</metadataPrefix>' in text
    assert '<metadataNamespace>http://www.openarchives.org/OAI/2.0/oai_dc/</metadataNamespace>' in text
    assert '<schema>http://arxiv.org/OAI/arXivRaw.xsd</schema>' in text
    assert '<ListMetadataFormats>' in text
    assert '<request verb="ListMetadataFormats" identifier="oai:arXiv.org:1001.3172">' in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/xml"
    assert response.headers["Surrogate-Control"] == "max-age=31536000"
    assert response.headers["Surrogate-Key"] == "oai" 
    text=response.get_data(as_text=True)
    assert "<error code=" not in text

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
