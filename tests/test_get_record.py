from oaipmh.data.oai_properties import OAIParams, OAIVerbs

def test_good_params(test_client):

    params = {OAIParams.VERB: OAIVerbs.GET_RECORD, OAIParams.ID: "oai:arXiv.org:0806.4129",  OAIParams.META_PREFIX: "oai_dc"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    assert response.headers["Content-Type"] == "text/xml"
    assert response.headers["Surrogate-Control"]==('max-age=800000')
    assert response.headers["Surrogate-Key"] == "paper-id-0806.4129 oai"
    text=response.get_data(as_text=True)
    assert "<error code=" not in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    assert response.headers["Content-Type"] == "text/xml"
    assert response.headers["Surrogate-Control"]==('max-age=800000')
    assert response.headers["Surrogate-Key"] == "paper-id-0806.4129 oai"
    text=response.get_data(as_text=True)
    assert "<error code=" not in text

def test_bad_meta_format(test_client):
    params = {OAIParams.VERB: OAIVerbs.GET_RECORD, OAIParams.ID: "oai:arXiv.org:2307.10651",  OAIParams.META_PREFIX: "pictures"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    assert response.headers["Content-Type"] == "text/xml"
    cache_timer=response.headers["Surrogate-Control"]
    assert cache_timer[:8]=='max-age='
    assert int(cache_timer[8:]) <= 3600*24
    assert response.headers["Surrogate-Key"] == "oai"
    text=response.get_data(as_text=True)
    assert "<error code='cannotDisseminateFormat'>" in text
    assert "Did not recognize requested format" in text

def test_special_char_encoding(test_client):
    response = test_client.get("/oai?verb=GetRecord&identifier=oai%3AarXiv.org%3Acs%2F0001024&metadataPrefix=oai_dc")
    assert response.status_code == 200
    assert "<error code='badArgument'>" not in response.text
    assert "<identifier>oai:arXiv.org:cs/0001024</identifier>" in response.text
    assert "A Parallel Algorithm for Dilated Contour Extraction from Bilevel Images" in response.text

def test_bad_id(test_client):

    params = {OAIParams.VERB: OAIVerbs.GET_RECORD, OAIParams.ID: "arXiv.org:2307.10651",  OAIParams.META_PREFIX: "oai_dc"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='idDoesNotExist'>" in text
    assert "All identifiers start with:" in text

def test_nonexistent_id(test_client):
    params = {OAIParams.VERB: OAIVerbs.GET_RECORD, OAIParams.ID: "oai:arXiv.org:2307.10651",  OAIParams.META_PREFIX: "oai_dc"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='idDoesNotExist'>" in text
    assert "Nothing found for this ID" in text

def test_extra_params(test_client):
    params = {OAIParams.VERB: OAIVerbs.GET_RECORD, OAIParams.ID: "oai:arXiv.org:2307.10651",  OAIParams.META_PREFIX: "oai_dc", "cookie":"chocolate"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" in text
    assert "Parameters provided did not match expected." in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" in text
    assert "Parameters provided did not match expected." in text

def test_missing_params(test_client):

    # missing metadata_prefix
    params = {OAIParams.VERB: OAIVerbs.GET_RECORD, OAIParams.ID: "oai:arXiv.org:2307.10651"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/xml"
    cache_timer=response.headers["Surrogate-Control"]
    assert cache_timer[:8]=='max-age='
    assert int(cache_timer[8:]) <= 3600*24
    assert response.headers["Surrogate-Key"] == "oai" 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" in text
    assert "Parameters provided did not match expected." in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" in text
    assert "Parameters provided did not match expected." in text

    # missing identifier
    params = {OAIParams.VERB: OAIVerbs.GET_RECORD, OAIParams.META_PREFIX: "oai_dc"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" in text
    assert "Parameters provided did not match expected." in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" in text
    assert "Parameters provided did not match expected." in text