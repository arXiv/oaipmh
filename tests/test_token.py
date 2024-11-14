from typing import Dict
import base64
import json
import pytest

from oaipmh.data.oai_errors import OAIBadResumptionToken
from oaipmh.processors.resume import ResToken

def test_token_encoding_decoding():
    params = {"verb": "GetRecord", "identifier": "12345"}
    res_token = ResToken(params=params, start_val=10)
    assert res_token.params== params
    assert res_token.start_val == 10
    encoded_token = res_token.to_token()
    assert isinstance(encoded_token, str)

    dict, num = ResToken.from_token(encoded_token)
    assert dict == params
    assert num == 10


def test_invalid_token_structure():
    invalid_data = {
        "not_params": {"verb": "GetRecord"},  
        "start_val": 10
    }
    encoded_invalid_token = base64.b64encode(json.dumps(invalid_data).encode("utf-8")).decode("utf-8")
    with pytest.raises(OAIBadResumptionToken, match="Token decoding failed or format is invalid."):
        ResToken.from_token(encoded_invalid_token)


def test_invalid_token_data_types():
    invalid_data = {
        "params": "not a dict", 
        "start_val": "not an int"  
    }
    encoded_invalid_token = base64.b64encode(json.dumps(invalid_data).encode("utf-8")).decode("utf-8")
    with pytest.raises(OAIBadResumptionToken, match="Token decoding failed or format is invalid."):
        ResToken.from_token(encoded_invalid_token)


def test_token_decoding_random_str():
    malformed_base64 = "not_a_valid_base64_string"
    with pytest.raises(OAIBadResumptionToken, match="Token decoding failed or format is invalid"):
        ResToken.from_token(malformed_base64)


def test_token_decoding_with_invalid_json():
    invalid_json_base64 = base64.b64encode(b"not valid json").decode("utf-8")
    with pytest.raises(OAIBadResumptionToken, match="Token decoding failed or format is invalid"):
        ResToken.from_token(invalid_json_base64)

    with pytest.raises(OAIBadResumptionToken, match="Token decoding failed or format is invalid"):
        ResToken.from_token("")


def test_extra_or_missing_keys_in_token():
    extra_key_data = {
        "params": {"verb": "GetRecord", "identifier": "12345"},
        "start_val": 10,
        "extra_key": "unexpected"
    }
    encoded_extra_key = base64.b64encode(json.dumps(extra_key_data).encode("utf-8")).decode("utf-8")
    with pytest.raises(OAIBadResumptionToken, match="Token decoding failed or format is invalid."):
        ResToken.from_token(encoded_extra_key)
    
    missing_key_data = {
        "params": {"verb": "GetRecord"}
    }
    encoded_missing_key = base64.b64encode(json.dumps(missing_key_data).encode("utf-8")).decode("utf-8")
    with pytest.raises(OAIBadResumptionToken, match="Token decoding failed or format is invalid."):
        ResToken.from_token(encoded_missing_key)