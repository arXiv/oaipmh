
from arxiv.taxonomy.definitions import GROUPS, ARCHIVES, CATEGORIES

from oaipmh.data.oai_properties import OAIParams, OAIVerbs
from oaipmh.processors.create_set_list import make_set_str

def test_output(test_client):
    #general case
    params = {OAIParams.VERB: OAIVerbs.LIST_SETS}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "test" not in text #test items
    assert "adap-org" not in text #inactive
    assert "<setSpec>math</setSpec>" in text
    assert "<setSpec>math:math</setSpec>" in text
    assert "<setSpec>math:math:NA</setSpec>" in text

def test_good_params(test_client):
    #general case
    params = {OAIParams.VERB: OAIVerbs.LIST_SETS}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/xml"
    assert response.headers["Surrogate-Control"] == "max-age=31536000"
    assert response.headers["Surrogate-Key"] == "oai-static oai" 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" not in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    assert response.headers["Content-Type"] == "text/xml"
    assert response.headers["Surrogate-Control"] == "max-age=31536000"
    assert response.headers["Surrogate-Key"] == "oai-static oai"
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" not in text

def test_extra_params(test_client):
    #general case
    params = {OAIParams.VERB: OAIVerbs.LIST_SETS, OAIParams.FROM:"now"}
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

    #extra with token
    params = {OAIParams.VERB: OAIVerbs.LIST_SETS, OAIParams.RES_TOKEN : "math", OAIParams.META_PREFIX:"rainbow"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" in text
    assert "No other paramters allowed with resumptionToken" in text

    #bad token
    params = {OAIParams.VERB: OAIVerbs.LIST_SETS, OAIParams.RES_TOKEN : "math"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" in text
    assert "Invalid token" in text

def test_make_set_str():
    assert 'physics'==make_set_str(GROUPS['grp_physics'])
    assert 'math'==make_set_str(GROUPS['grp_math'])
    assert 'math:math' == make_set_str(ARCHIVES['math'])
    assert 'physics:hep-ph' == make_set_str(ARCHIVES['hep-ph'])
    assert 'physics:physics:flu-dyn' == make_set_str(CATEGORIES['physics.flu-dyn'])
    assert 'cs:cs:GT' == make_set_str(CATEGORIES['cs.GT'])
    assert 'physics:astro-ph'==make_set_str(CATEGORIES['astro-ph'])
  