#runs tests for the code list_records and list_indetifiers share


from oaipmh.data.oai_properties import OAIParams, OAIVerbs

def test_good_params(test_client):
    #good minimal params
    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.META_PREFIX: "oai_dc"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" not in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" not in text

    #good maximal params
    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc", OAIParams.FROM: "2020-01-05", OAIParams.UNTIL:"2020-02-05", OAIParams.SET: "math"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" not in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" not in text

    #good partial params
    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.META_PREFIX: "oai_dc", OAIParams.UNTIL:"2020-02-05", OAIParams.SET: "math"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" not in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" not in text

def test_extra_params(test_client):
    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc", "color":"green"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" in text
    assert "Unallowed parameter." in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" in text
    assert "Unallowed parameter." in text

def test_bad_meta_format(test_client):
    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.META_PREFIX: "pictures"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='cannotDisseminateFormat'>" in text
    assert "Did not recognize requested format" in text

def test_bad_date_params(test_client):

    #invalid from types
    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc", OAIParams.FROM: "a/37", OAIParams.UNTIL:"2020-02-05", OAIParams.SET: "math"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>"  in text
    assert "from date format must be YYYY-MM-DD" in text

    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc", OAIParams.FROM: "2020-5-6", OAIParams.UNTIL:"2020-02-05", OAIParams.SET: "math"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>"  in text
    assert "from date format must be YYYY-MM-DD" in text

    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc", OAIParams.FROM: "2024-11-08T19:49:17Z", OAIParams.UNTIL:"2020-02-05", OAIParams.SET: "math"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>"  in text
    assert "from date format must be YYYY-MM-DD" in text

    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc", OAIParams.FROM: "2024-32-08", OAIParams.UNTIL:"2020-02-05", OAIParams.SET: "math"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>"  in text
    assert "from date format must be YYYY-MM-DD" in text

    #invalid until types
    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc", OAIParams.UNTIL: "a/37", OAIParams.FROM:"2020-02-05", OAIParams.SET: "math"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>"  in text
    assert "until date format must be YYYY-MM-DD" in text

    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc", OAIParams.UNTIL: "2020-5-6", OAIParams.FROM:"2020-02-05", OAIParams.SET: "math"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>"  in text
    assert "until date format must be YYYY-MM-DD" in text

    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc", OAIParams.UNTIL: "2024-11-08T19:49:17Z", OAIParams.FROM:"2020-02-05", OAIParams.SET: "math"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>"  in text
    assert "until date format must be YYYY-MM-DD" in text

    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc", OAIParams.UNTIL: "2024-32-08", OAIParams.FROM:"2020-02-05", OAIParams.SET: "math"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>"  in text
    assert "until date format must be YYYY-MM-DD" in text


def test_token_params(test_client):
    #correct params
    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.RES_TOKEN: "rainbow"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" not in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" not in text

    #cant have other valid params along with token
    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.RES_TOKEN: "rainbow",  OAIParams.META_PREFIX: "oai_dc"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" in text
    assert "No other paramters allowed with" in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" in text
    assert "No other paramters allowed with" in text
