#runs tests for the code list_records and list_indetifiers share
import pytest
from unittest.mock import patch
from datetime import datetime
from typing import Dict

from arxiv.taxonomy.definitions import GROUPS, ARCHIVES, CATEGORIES

from oaipmh.data.oai_config import SUPPORTED_METADATA_FORMATS
from oaipmh.data.oai_properties import OAIParams, OAIVerbs
from oaipmh.data.oai_errors import OAIBadArgument
from oaipmh.processors.fetch_list import create_records, fetch_list
from oaipmh.processors.resume import ResToken
from oaipmh.requests.data_queries import _parse_set
from oaipmh.serializers.create_records import Header, arXivOldRecord, arXivRawRecord, arXivRecord, dcRecord

def test_good_params(test_client):
    #good minimal params
    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.META_PREFIX: "oai_dc"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    assert response.headers["Content-Type"] == "application/xml"
    cache_header= response.headers["Surrogate-Control"]
    assert cache_header[0:8]==('max-age=')
    assert int(cache_header[8:])<= 60*60*24
    assert response.headers["Surrogate-Key"] == "oai" 
    text=response.get_data(as_text=True)
    assert "<error code=" not in text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200 
    assert response.headers["Content-Type"] == "application/xml"
    cache_header= response.headers["Surrogate-Control"]
    assert cache_header[0:8]==('max-age=')
    assert int(cache_header[8:])<= 60*60*24
    assert response.headers["Surrogate-Key"] == "oai" 
    text=response.get_data(as_text=True)
    assert "<error code=" not in text

    #good maximal params
    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc", OAIParams.FROM: "2009-01-05", OAIParams.UNTIL:"2020-02-05", OAIParams.SET: "math"}
    response = test_client.get("/oai", query_string=params)
    assert response.headers["Content-Type"] == "application/xml"
    cache_header= response.headers["Surrogate-Control"]
    assert cache_header[0:8]==('max-age=')
    assert int(cache_header[8:])<= 60*60*24
    assert response.headers["Surrogate-Key"] == "oai" 
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" not in text

    response = test_client.post("/oai", data=params)
    assert response.headers["Content-Type"] == "application/xml"
    cache_header= response.headers["Surrogate-Control"]
    assert cache_header[0:8]==('max-age=')
    assert int(cache_header[8:])<= 60*60*24
    assert response.headers["Surrogate-Key"] == "oai" 
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" not in text

    #good partial params
    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.META_PREFIX: "oai_dc", OAIParams.UNTIL:"2020-02-05", OAIParams.SET: "math"}
    response = test_client.get("/oai", query_string=params)
    assert response.headers["Content-Type"] == "application/xml"
    cache_header= response.headers["Surrogate-Control"]
    assert cache_header[0:8]==('max-age=')
    assert int(cache_header[8:])<= 60*60*24
    assert response.headers["Surrogate-Key"] == "oai" 
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" not in text

    response = test_client.post("/oai", data=params)
    assert response.headers["Content-Type"] == "application/xml"
    cache_header= response.headers["Surrogate-Control"]
    assert cache_header[0:8]==('max-age=')
    assert int(cache_header[8:])<= 60*60*24
    assert response.headers["Surrogate-Key"] == "oai" 
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

def test_no_meta_format(test_client):
    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code='badArgument'>" in text
    assert "metadataPrefix required" in text

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

def test_create_headers_list(metadata_object2, metadata_object3):
    #identifier requests only fetch the current version
    data=[ metadata_object2, metadata_object3]
    expected=[
        Header("1234.56789", datetime(2023,3,1,15,7,8),[CATEGORIES['cs.AI'], CATEGORIES['hep-lat']]),
        Header("1234.56790", datetime(2024,3,7,15,7,8),[CATEGORIES['cs.LG'], CATEGORIES['hep-lat']])
    ]
    result= create_records(data, True, SUPPORTED_METADATA_FORMATS['arXiv'])
    assert expected == result
    result= create_records(data, True, SUPPORTED_METADATA_FORMATS['arXivRaw'])
    assert expected == result

def test_create_records_list(metadata_object1, metadata_object2, metadata_object3):
    #arXiv and arXiv old only use the current copy of metadata
    data=[ metadata_object2, metadata_object3]
    result= create_records(data, False, SUPPORTED_METADATA_FORMATS['arXiv'])
    expected=[arXivRecord(metadata_object2), arXivRecord(metadata_object3)]
    assert result==expected

    result= create_records(data, False, SUPPORTED_METADATA_FORMATS['arXivOld'])
    expected=[arXivOldRecord(metadata_object2), arXivOldRecord(metadata_object3)]
    assert result==expected

    #oai_dc and arXivRaw use all versions of metadata
    data=[ metadata_object1, metadata_object2, metadata_object3]
    result= create_records(data, False, SUPPORTED_METADATA_FORMATS['arXivRaw'])
    expected=[arXivRawRecord([metadata_object1, metadata_object2]), arXivRawRecord([metadata_object3])]
    assert result==expected

    result= create_records(data, False, SUPPORTED_METADATA_FORMATS['oai_dc'])
    expected=[dcRecord([metadata_object1, metadata_object2]), dcRecord([metadata_object3])]
    assert result==expected

    #can handle other orders of versions so long as they are all together
    data=[metadata_object3, metadata_object2, metadata_object1]
    result= create_records(data, False, SUPPORTED_METADATA_FORMATS['arXivRaw'])
    expected=[arXivRawRecord([metadata_object1, metadata_object2]), arXivRawRecord([metadata_object3])]
    result.sort() 
    assert result==expected

    result= create_records(data, False, SUPPORTED_METADATA_FORMATS['oai_dc'])
    expected=[dcRecord([metadata_object1, metadata_object2]), dcRecord([metadata_object3])]
    result.sort() 
    assert result==expected

def test_no_res_token_needed(test_client):
    with patch('oaipmh.processors.fetch_list.IDENTIFIERS_LIMIT', 1000):
        params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc"}
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200 
        text=response.get_data(as_text=True)
        assert "resumptionToken" not in text
    
def test_enforces_limits(test_client):
    with patch('oaipmh.processors.fetch_list.IDENTIFIERS_LIMIT', 10):
        params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc"}
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200 
        text=response.get_data(as_text=True)
        assert "resumptionToken" in text
        assert text.count('<header>') == 10

    with patch('oaipmh.processors.fetch_list.IDENTIFIERS_LIMIT', 10):
        params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.META_PREFIX: "oai_dc"}
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200 
        text=response.get_data(as_text=True)
        assert "resumptionToken" not in text
        assert text.count('<header>') > 10

    with patch('oaipmh.processors.fetch_list.RECORDS_LIMIT', 10):
        params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc"}
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200 
        text=response.get_data(as_text=True)
        assert "resumptionToken" not in text
        assert text.count('<header>') > 10

    with patch('oaipmh.processors.fetch_list.RECORDS_LIMIT', 10):
        params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.META_PREFIX: "oai_dc"}
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200 
        text=response.get_data(as_text=True)
        assert "resumptionToken" in text
        assert text.count('<header>') == 10

def __get_res_token(text:str)-> str:
    import xml.etree.ElementTree as ET
    root = ET.fromstring(text)
    namespace = {'oai': 'http://www.openarchives.org/OAI/2.0/'}
    resumption_token = root.find('.//oai:resumptionToken', namespace)
    return resumption_token.text or ''

def test_resumption_sequencing1(test_client):
    #makes sure a sequence doesnt miss anything
    limit=2
    with patch('oaipmh.processors.fetch_list.IDENTIFIERS_LIMIT', limit):
        params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc"}
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200 
        text=response.get_data(as_text=True)
        assert "resumptionToken" in text
        assert text.count("<header>")==limit
        assert '<identifier>oai:arXiv.org:chao-dyn/9510015</identifier>' in text
        assert '<identifier>oai:arXiv.org:hep-th/9901002</identifier>' in text
        token=__get_res_token(text)
        assert token[-1] == '0' #could change with different token ecnoding scheme

        params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.RES_TOKEN: token}
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200 
        text=response.get_data(as_text=True)
        assert "resumptionToken" in text
        assert text.count("<header>")==limit
        assert '<identifier>oai:arXiv.org:0704.0046</identifier>' in text
        assert '<identifier>oai:arXiv.org:1008.3222</identifier>' in text
        token=__get_res_token(text)
        assert token[-1] == '0' #could change with different token ecnoding scheme

        """a note on the following results: 
        if you generate a large list of identifiers, the upcoming expected papers will NOT be the next two in the list. 
        Both the list from the database and the list presented to users are sorted first by their timestamp, then by paper_id.
        However, the list displayed to the end user is sorted by the timestamp to the resolution of a day where the database sorting resolution is down to the second.
        This means that the database will cut off a paper with an earlier paper_id that was modified at a later time on the same date.
        This is expected behavior, but may look funny at very low limit chunks where all papers have the same date. 
        """

        params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.RES_TOKEN: token}
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200 
        text=response.get_data(as_text=True)
        assert "resumptionToken" in text
        assert text.count("<header>")==limit
        #TODO im pretty sure 1102.0299 should be here
        assert '<identifier>oai:arXiv.org:0811.2813</identifier>' not in text #would be next in a bigger list
        assert '<identifier>oai:arXiv.org:1102.0299</identifier>' in text
        assert '<identifier>oai:arXiv.org:1102.0285</identifier>' in text
        token=__get_res_token(text)
        assert token[-1] == '2' #could change with different token ecnoding scheme

        params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.RES_TOKEN: token}
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200 
        text=response.get_data(as_text=True)
        assert "resumptionToken" in text
        assert text.count("<header>")==limit
        assert '<identifier>oai:arXiv.org:0901.0022</identifier>' in text
        assert '<identifier>oai:arXiv.org:1001.2600</identifier>' in text
        assert '<identifier>oai:arXiv.org:1102.0304</identifier>' not in text #has the same modtime as 1001.2600 but later in paper_id ordering
        token=__get_res_token(text)
        assert token[-1] == '4' #could change with different token ecnoding scheme
     
def test_resumption_sequencing2(test_client):
    #more testing a sequence doesnt miss things at different breakpoints
    limit=3
    with patch('oaipmh.processors.fetch_list.IDENTIFIERS_LIMIT', limit):
        params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc"}
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200 
        text=response.get_data(as_text=True)
        assert "resumptionToken" in text
        assert text.count("<header>")==limit
        assert '<identifier>oai:arXiv.org:chao-dyn/9510015</identifier>' in text
        assert '<identifier>oai:arXiv.org:hep-th/9901002</identifier>' in text
        assert '<identifier>oai:arXiv.org:0704.0046</identifier>' in text
        token=__get_res_token(text)
        assert token[-1] == '0' #could change with different token ecnoding scheme

        params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.RES_TOKEN: token}
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200 
        text=response.get_data(as_text=True)
        assert "resumptionToken" in text
        assert text.count("<header>")==limit
        assert '<identifier>oai:arXiv.org:1102.0299</identifier>' in text
        assert '<identifier>oai:arXiv.org:1102.0285</identifier>' in text
        assert '<identifier>oai:arXiv.org:1008.3222</identifier>' in text
        token=__get_res_token(text)
        assert token[-1] == '2' #could change with different token ecnoding scheme

        params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.RES_TOKEN: token}
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200 
        text=response.get_data(as_text=True)
        assert "resumptionToken" in text
        assert text.count("<header>")==limit
        assert '<identifier>oai:arXiv.org:0901.0022</identifier>' in text
        assert '<identifier>oai:arXiv.org:1001.2600</identifier>' in text
        assert '<identifier>oai:arXiv.org:1102.0304</identifier>' in text
        token=__get_res_token(text)
        assert token[-1] == '5' #could change with different token ecnoding scheme

def test_resumption_sequencing_records(test_client):
    #makes sure a sequence doesnt miss anything
    limit=2
    with patch('oaipmh.processors.fetch_list.RECORDS_LIMIT', limit):
        params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.META_PREFIX: "oai_dc"}
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200 
        text=response.get_data(as_text=True)
        assert "resumptionToken" in text
        assert text.count("<header>")==limit
        assert '<identifier>oai:arXiv.org:chao-dyn/9510015</identifier>' in text
        assert '<identifier>oai:arXiv.org:hep-th/9901002</identifier>' in text
        token=__get_res_token(text)
        assert token[-1] == '0' #could change with different token ecnoding scheme

        params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.RES_TOKEN: token}
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200 
        text=response.get_data(as_text=True)
        assert "resumptionToken" in text
        assert text.count("<header>")==limit
        assert '<identifier>oai:arXiv.org:0704.0046</identifier>' in text
        assert '<identifier>oai:arXiv.org:1008.3222</identifier>' in text
        token=__get_res_token(text)
        assert token[-1] == '0' #could change with different token ecnoding scheme

        params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.RES_TOKEN: token}
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200 
        text=response.get_data(as_text=True)
        assert "resumptionToken" in text
        assert text.count("<header>")==limit
        #TODO im pretty sure 1102.0299 should be here
        assert '<identifier>oai:arXiv.org:0811.2813</identifier>' not in text #would be next in a bigger list
        assert '<identifier>oai:arXiv.org:1102.0299</identifier>' in text
        assert '<identifier>oai:arXiv.org:1102.0285</identifier>' in text
        token=__get_res_token(text)
        assert token[-1] == '2' #could change with different token ecnoding scheme

        params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.RES_TOKEN: token}
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200 
        text=response.get_data(as_text=True)
        assert "resumptionToken" in text
        assert text.count("<header>")==limit
        assert '<identifier>oai:arXiv.org:0901.0022</identifier>' in text
        assert '<identifier>oai:arXiv.org:1001.2600</identifier>' in text
        assert '<identifier>oai:arXiv.org:1102.0304</identifier>' not in text #has the same modtime as 1001.2600 but later in paper_id ordering
        token=__get_res_token(text)
        assert token[-1] == '4' #could change with different token ecnoding scheme
  

#formatting
def test_records_from_params(test_client):
    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.META_PREFIX: "arXiv", OAIParams.FROM: "2009-01-05", OAIParams.UNTIL:"2020-02-05", OAIParams.SET: "math"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" not in text
    assert '<ListRecords>' in text
    assert '<request verb="ListRecords" metadataPrefix="arXiv" from="2009-01-05" until="2020-02-05" set="math">' in text
    assert '<identifier>oai:arXiv.org:0704.0046</identifier>' in text
    assert  text.count("<record>")==4 #could change if more data gets added to test database
    assert '<id>0806.4129</id>' in text
    assert '<doi>10.1007/s00205-010-0322-x</doi>' in text

def test_records_starting_from_token(test_client):
    query_data: Dict[OAIParams,str]={
        OAIParams.VERB:OAIVerbs.LIST_RECORDS,
        OAIParams.FROM:'2019-10-11',
        OAIParams.UNTIL:'2024-12-03',
        OAIParams.META_PREFIX:'oai_dc'
    }
    token=ResToken(query_data, 2)

    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.RES_TOKEN: token.token_str}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" not in text
    assert "<request verb='ListRecords' resumptionToken='" in text
    assert 'verb%3DListRecords%26from%3D2019-10-11%26until%3D2024-12-03%26metadataPrefix%3Doai_dc%26skip%3D2' in text
    assert '<ListRecords>' in text
    assert  text.count("<record>")==5 #could change if more data gets added to test database
    assert '<identifier>oai:arXiv.org:1102.0372</identifier>' in text
    assert '<dc:title>Lattice polygons and families of curves on rational surfaces</dc:title>' in text
    assert '<dc:identifier>http://arxiv.org/abs/2305.11452</dc:identifier>' in text

    assert '<identifier>oai:arXiv.org:1102.0366</identifier>' not in text #first entry should be skipped
    assert 'oai:arXiv.org:1005.1251' not in text #second entry should be skipped

def test_identifiers_from_params(test_client):
    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "arXiv", OAIParams.FROM: "2009-01-05", OAIParams.UNTIL:"2020-02-05", OAIParams.SET: "math"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" not in text
    assert '<ListIdentifiers>' in text
    assert '<request verb="ListIdentifiers" metadataPrefix="arXiv" from="2009-01-05" until="2020-02-05" set="math">' in text
    assert '<identifier>oai:arXiv.org:0704.0046</identifier>' in text
    assert  text.count("<identifier>")==4 #could change if more data gets added to test database
    assert "<record>" not in text
    assert '<id>0806.4129</id>' not in text
    assert '<doi>10.1007/s00205-010-0322-x</doi>'not in text

def test_identifiers_starting_from_token(test_client):
    query_data: Dict[OAIParams,str]={
        OAIParams.VERB:OAIVerbs.LIST_IDS,
        OAIParams.FROM:'2019-10-11',
        OAIParams.UNTIL:'2024-12-03',
        OAIParams.META_PREFIX:'oai_dc'
    }
    token=ResToken(query_data, 2)

    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.RES_TOKEN: token.token_str}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<error code=" not in text
    assert "<request verb='ListIdentifiers' resumptionToken='" in text
    assert 'verb%3DListIdentifiers%26from%3D2019-10-11%26until%3D2024-12-03%26metadataPrefix%3Doai_dc%26skip%3D2' in text
    assert '<ListIdentifiers>' in text
    assert  text.count("<identifier>")==5 #could change if more data gets added to test database
    assert '<record>' not in text
    assert '<identifier>oai:arXiv.org:1102.0372</identifier>' in text
    assert '<dc:title>Lattice polygons and families of curves on rational surfaces</dc:title>' not in text
    assert '<dc:identifier>http://arxiv.org/abs/2305.11452</dc:identifier>' not in text

    assert '<identifier>oai:arXiv.org:1102.0366</identifier>' not in text #first entry should be skipped
    assert 'oai:arXiv.org:1005.1251' not in text #second entry should be skipped

