from unittest.mock import patch

def test_get_record(test_client):
    params = {"verb": "GetRecord", "identifier": "oai:example.org:record123"}

    with patch('oaipmh.requests.verb_sorter.get_record') as mock_get_record:
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200
        mock_get_record.assert_called_once_with(params)

    with patch('oaipmh.requests.verb_sorter.get_record') as mock_get_record:
        response = test_client.post("/oai", data=params)
        assert response.status_code == 200
        mock_get_record.assert_called_once_with(params)

def test_list_records(test_client):
    params = {"verb": "ListRecords", "metadataPrefix": "oai_dc"}
    
    with patch('oaipmh.requests.verb_sorter.list_records') as mock_list_records:
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200
        mock_list_records.assert_called_once_with(params)

    with patch('oaipmh.requests.verb_sorter.list_records') as mock_list_records:
        response = test_client.post("/oai", data=params)
        assert response.status_code == 200
        mock_list_records.assert_called_once_with(params)

def test_list_identifiers(test_client):
    params = {"verb": "ListIdentifiers", "metadataPrefix": "oai_dc"}
    
    with patch('oaipmh.requests.verb_sorter.list_identifiers') as mock_list_identifiers:
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200
        mock_list_identifiers.assert_called_once_with(params)

    with patch('oaipmh.requests.verb_sorter.list_identifiers') as mock_list_identifiers:
        response = test_client.post("/oai", data=params)
        assert response.status_code == 200
        mock_list_identifiers.assert_called_once_with(params)

def test_identify(test_client):
    params = {"verb": "Identify"}

    with patch('oaipmh.requests.verb_sorter.identify') as mock_identify:
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200
        mock_identify.assert_called_once_with(params)

    with patch('oaipmh.requests.verb_sorter.identify') as mock_identify:
        response = test_client.post("/oai", data=params)
        assert response.status_code == 200
        mock_identify.assert_called_once_with(params)

def test_list_metadata_formats(test_client):
    params = {"verb": "ListMetadataFormats"}
    
    with patch('oaipmh.requests.verb_sorter.list_metadata_formats') as mock_list_metadata_formats:
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200
        mock_list_metadata_formats.assert_called_once_with(params)

    with patch('oaipmh.requests.verb_sorter.list_metadata_formats') as mock_list_metadata_formats:
        response = test_client.post("/oai", data=params)
        assert response.status_code == 200
        mock_list_metadata_formats.assert_called_once_with(params)

def test_list_sets(test_client):
    params = {"verb": "ListSets"}
    
    with patch('oaipmh.requests.verb_sorter.list_sets') as mock_list_sets:
        response = test_client.get("/oai", query_string=params)
        assert response.status_code == 200
        mock_list_sets.assert_called_once_with(params)

    with patch('oaipmh.requests.verb_sorter.list_sets') as mock_list_sets:
        response = test_client.post("/oai", data=params)
        assert response.status_code == 200
        mock_list_sets.assert_called_once_with(params)

def test_no_verb(test_client):
    params = {"not_verb": "ListSets"}
    
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200
    assert "<error code='badVerb'>" in response.text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200
    assert "<error code='badVerb'>" in response.text

def test_bad_verb(test_client):
    params = {"verb": "chaos!"}
    
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200
    assert "<error code='badVerb'>" in response.text

    response = test_client.post("/oai", data=params)
    assert response.status_code == 200
    assert "<error code='badVerb'>" in response.text