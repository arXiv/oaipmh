from oaipmh.data.oai_properties import OAIParams, OAIVerbs

def test_good_params(test_client):
    params = {OAIParams.VERB: OAIVerbs.IDENTIFY}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" not in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" not in text

def test_extra_params(test_client):
    params = {OAIParams.VERB: OAIVerbs.IDENTIFY, OAIParams.ID: "oai:example.org:record123"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" in text
    assert "No other parameters allowed" in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" in text
    assert "No other parameters allowed" in text

def test_contents(test_client):
    params = {OAIParams.VERB: OAIVerbs.IDENTIFY}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    assert response.headers["Content-Type"] == "application/xml"
    assert response.headers["Surrogate-Control"] == "max-age=31536000"
    assert response.headers["Surrogate-Key"] == "oai"

    text=response.get_data(as_text=True)
    assert "<repositoryName>arXiv</repositoryName>" in text
    assert "<baseURL>https://arxiv.org/oai</baseURL>" in text
    assert "<earliestDatestamp>1997-01-30</earliestDatestamp>" in text
    assert "<granularity>YYYY-MM-DD</granularity>" in text
    assert "<description>" in text
    assert "<text>Full-content harvesting not permitted (except by special arrangement)</text>" in text
    assert "<URL>http://arxiv.org/help/oa/metadataPolicy</URL>" in text

