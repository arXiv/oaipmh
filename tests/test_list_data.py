#runs tests for the code list_records and list_indetifiers share
import pytest
from typing import Dict

from arxiv.taxonomy.definitions import GROUPS, ARCHIVES, CATEGORIES

from oaipmh.data.oai_properties import OAIParams, OAIVerbs
from oaipmh.data.oai_errors import OAIBadArgument
from oaipmh.processors.resume import ResToken
from oaipmh.requests.data_queries import _parse_set

def test_good_params(test_client):
    #good minimal params
    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.META_PREFIX: "oai_dc"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" not in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" not in text

    #good maximal params
    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc", OAIParams.FROM: "2009-01-05", OAIParams.UNTIL:"2020-02-05", OAIParams.SET: "math"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" not in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" not in text

    #good partial params
    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.META_PREFIX: "oai_dc", OAIParams.UNTIL:"2020-02-05", OAIParams.SET: "math"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" not in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" not in text

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

    #start later than end
    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc", OAIParams.UNTIL: "2024-02-08", OAIParams.FROM:"2024-03-05", OAIParams.SET: "math"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>"  in text
    assert "until date must be greater than or equal to from date" in text

    #start too early
    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc", OAIParams.UNTIL: "2024-02-08", OAIParams.FROM:"2001-03-05", OAIParams.SET: "math"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>"  in text
    assert "start date too early" in text

    #dates in the future
    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc", OAIParams.UNTIL: "2624-02-08", OAIParams.FROM:"2024-03-05", OAIParams.SET: "math"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>"  in text
    assert "until date too late" in text
    

def test_bad_set_params(test_client):
    #not a valid set combo
    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc", OAIParams.SET: "math:physics"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>"  in text
    assert "Set does not exist" in text

    #test category
    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc", OAIParams.SET: "test:test"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>"  in text
    assert "Invalid set request" in text

    #inactive category
    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc", OAIParams.SET: "physics:adap-org"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>"  in text
    assert "Set does not exist" in text

def test_token_params(test_client):
    #invalid token
    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.RES_TOKEN: "rainbow"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" in text

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

    #invalid token
    query_data: Dict[OAIParams,str]={
        OAIParams.VERB:OAIVerbs.LIST_RECORDS,
        OAIParams.ID:'1234.5678', #not allowed
        OAIParams.FROM:'10-11-2023',
        OAIParams.UNTIL:'12-03-2023',
        OAIParams.META_PREFIX:'oai_dc',
    }
    token=ResToken(query_data, 300)

    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.RES_TOKEN: token.token_str}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" in text

    #valid token
    query_data: Dict[OAIParams,str]={
        OAIParams.VERB:OAIVerbs.LIST_RECORDS,
        OAIParams.FROM:'2010-09-11',
        OAIParams.SET:'math',
        OAIParams.META_PREFIX:'oai_dc',
    }
    token=ResToken(query_data, 1)

    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.RES_TOKEN: token.token_str}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" not in text
    assert "<request verb='ListRecords' resumptionToken='" in text
    assert 'verb%3DListRecords%26from%3D2010-09-11%26set%3Dmath%26metadataPrefix%3Doai_dc%26skip%3D1' in text

    query_data: Dict[OAIParams,str]={
        OAIParams.VERB:OAIVerbs.LIST_RECORDS,
        OAIParams.FROM:'2008-10-11',
        OAIParams.UNTIL:'2023-12-03',
        OAIParams.META_PREFIX:'oai_dc',
    }
    token=ResToken(query_data, 1)

    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.RES_TOKEN: token.token_str}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" not in text
    assert "<request verb='ListRecords' resumptionToken='" in text
    assert 'verb%3DListRecords%26from%3D2008-10-11%26until%3D2023-12-03%26metadataPrefix%3Doai_dc%26skip%3D1' in text

    #include res token in token
    query_data: Dict[OAIParams,str]={
        OAIParams.VERB:OAIVerbs.LIST_RECORDS,
        OAIParams.FROM:'2023-10-11',
        OAIParams.UNTIL:'2023-12-03',
        OAIParams.META_PREFIX:'oai_dc',
        OAIParams.RES_TOKEN:token.token_str
    }
    token=ResToken(query_data, 300)

    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.RES_TOKEN: token.token_str}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" in text
    assert "<request verb='ListRecords' resumptionToken='" in text
    assert 'verb%3DListRecords%26from%3D2023-10-11%26until%3D2023-12-03%26metadataPrefix%3Doai_dc%26skip%3D300' in text

    #start val isnt int
    token=ResToken(query_data, "cat")
    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.RES_TOKEN: token.token_str}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" in text

    #res token doesnt have right type as new request
    query_data: Dict[OAIParams,str]={
        OAIParams.VERB:OAIVerbs.LIST_IDS,
        OAIParams.FROM:'2023-10-11',
        OAIParams.SET:'cs',
        OAIParams.META_PREFIX:'oai_dc',
    }
    token=ResToken(query_data, 300)

    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.RES_TOKEN: token.token_str}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badResumptionToken'" in text

def test_set_parser():
    #good values
    assert _parse_set('physics') == GROUPS['grp_physics'] 
    assert _parse_set('physics:physics') == ARCHIVES['physics']
    assert _parse_set('physics:physics:flu-dyn') == CATEGORIES['physics.flu-dyn']

    #bad values
    #gibberish
    with pytest.raises(OAIBadArgument, match="Set does not exist"):
        _parse_set("2020-5-6")  
    with pytest.raises(OAIBadArgument, match="Set does not exist"):
        _parse_set("maths")
    with pytest.raises(OAIBadArgument, match="Set does not exist"):
        _parse_set("math:nonsense")
    with pytest.raises(OAIBadArgument, match="Set does not exist"):
        _parse_set("math:math:nonsense")
    with pytest.raises(OAIBadArgument, match="Set does not exist"):
        _parse_set("nonsense:math")
    with pytest.raises(OAIBadArgument, match="Set does not exist"):
        _parse_set("nonsense:math:NA")
    with pytest.raises(OAIBadArgument, match="Set does not exist"):
        _parse_set("math:nonsense:NA")

    with pytest.raises(OAIBadArgument, match="Set has too many levels"):
        _parse_set("math:math:math:NA")

    #incorrect structure
    with pytest.raises(OAIBadArgument, match="Set does not exist"):
        _parse_set("math:math:flu-dyn")
    with pytest.raises(OAIBadArgument, match="Set does not exist"):
        _parse_set("math:physics:flu-dyn")
    with pytest.raises(OAIBadArgument, match="Set does not exist"):
        _parse_set("math:nucl-th")

