from unittest.mock import patch

from oaipmh.data.oai_properties import OAIVerbs, OAIParams

def test_get_record(test_client):
    params = {OAIParams.VERB: OAIVerbs.GET_RECORD, OAIParams.ID: "oai:example.org:record123"}

    with patch('oaipmh.requests.verb_sorter.get_record', return_value=("working", 200, {})) as mock_get_record:
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200
        mock_get_record.assert_called_once_with(params)

    with patch('oaipmh.requests.verb_sorter.get_record', return_value=("working", 200, {})) as mock_get_record:
        response = test_client.post("/oai", data=params)
        assert response.status_code == 200
        mock_get_record.assert_called_once_with(params)

def test_list_records(test_client):
    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.META_PREFIX: "oai_dc"}
    
    with patch('oaipmh.requests.verb_sorter.list_records', return_value=("working", 200, {})) as mock_list_records:
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200
        mock_list_records.assert_called_once_with(params)

    with patch('oaipmh.requests.verb_sorter.list_records', return_value=("working", 200, {})) as mock_list_records:
        response = test_client.post("/oai", data=params)
        assert response.status_code == 200
        mock_list_records.assert_called_once_with(params)

def test_list_identifiers(test_client):
    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX: "oai_dc"}
    
    with patch('oaipmh.requests.verb_sorter.list_identifiers', return_value=("working", 200, {})) as mock_list_identifiers:
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200
        mock_list_identifiers.assert_called_once_with(params)

    with patch('oaipmh.requests.verb_sorter.list_identifiers', return_value=("working", 200, {})) as mock_list_identifiers:
        response = test_client.post("/oai", data=params)
        assert response.status_code == 200
        mock_list_identifiers.assert_called_once_with(params)

def test_identify(test_client):
    params = {OAIParams.VERB: OAIVerbs.IDENTIFY}

    with patch('oaipmh.requests.verb_sorter.identify', return_value=("working", 200, {})) as mock_identify:
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200
        mock_identify.assert_called_once_with(params)

    with patch('oaipmh.requests.verb_sorter.identify', return_value=("working", 200, {})) as mock_identify:
        response = test_client.post("/oai", data=params)
        assert response.status_code == 200
        mock_identify.assert_called_once_with(params)

def test_list_metadata_formats(test_client):
    params = {OAIParams.VERB: OAIVerbs.LIST_META_FORMATS}
    
    with patch('oaipmh.requests.verb_sorter.list_metadata_formats', return_value=("working", 200, {})) as mock_list_metadata_formats:
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200
        mock_list_metadata_formats.assert_called_once_with(params)

    with patch('oaipmh.requests.verb_sorter.list_metadata_formats', return_value=("working", 200, {})) as mock_list_metadata_formats:
        response = test_client.post("/oai", data=params)
        assert response.status_code == 200
        mock_list_metadata_formats.assert_called_once_with(params)

def test_list_sets(test_client):
    params = {OAIParams.VERB: OAIVerbs.LIST_SETS}
    
    with patch('oaipmh.requests.verb_sorter.list_sets', return_value=("working", 200, {})) as mock_list_sets:
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200
        mock_list_sets.assert_called_once_with(params)

    with patch('oaipmh.requests.verb_sorter.list_sets', return_value=("working", 200, {})) as mock_list_sets:
        response = test_client.post("/oai", data=params)
        assert response.status_code == 200
        mock_list_sets.assert_called_once_with(params)

def test_no_verb(test_client):
    params = {"not_verb": OAIVerbs.LIST_SETS}
    
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200
    assert "<error code='badVerb'>" in response.text
    assert "Invalid verb provided" in response.text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200
    assert "<error code='badVerb'>" in response.text
    assert "Invalid verb provided" in response.text

def test_bad_verb(test_client):
    params = {OAIParams.VERB: "chaos!"}
    
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200
    assert "<error code='badVerb'>" in response.text
    assert "Invalid verb provided" in response.text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200
    assert "<error code='badVerb'>" in response.text
    assert "Invalid verb provided" in response.text