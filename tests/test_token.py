
import base64
import json
from datetime import datetime
import pytest
from urllib.parse import urlencode, quote, unquote, parse_qs

from oaipmh.data.oai_errors import OAIBadResumptionToken
from oaipmh.data.oai_properties import OAIParams, OAIVerbs
from oaipmh.processors.resume import ResToken

def test_token_encoding_decoding():
    unallowed_chars=['/','?','#','=','&',':',';',' ','+']

    #minimal params
    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.META_PREFIX:'oai_dc'}
    res_token = ResToken(params=params, start_val=0)
    assert res_token.params== params
    assert res_token.start_val == 0
    assert res_token.expires.hour==0
    assert res_token.expires.minute==0
    encoded_token = res_token.to_token()
    assert isinstance(encoded_token, str)
    assert not any(char in encoded_token for char in unallowed_chars)

    dict, num = ResToken.from_token(encoded_token)
    assert dict == params
    assert num == 0

    #maximal params
    params = {OAIParams.VERB: OAIVerbs.LIST_IDS, OAIParams.META_PREFIX:'arXiv', OAIParams.FROM:'2011-10-08', OAIParams.UNTIL:'2013-10-08', OAIParams.SET:"math:math.NA"}
    res_token = ResToken(params=params, start_val=33)
    assert res_token.params== params
    assert res_token.start_val == 33
    encoded_token = res_token.to_token()
    assert isinstance(encoded_token, str)
    assert not any(char in encoded_token for char in unallowed_chars)

    dict, num = ResToken.from_token(encoded_token)
    assert dict == params
    assert num ==33

def test_invalid_token_structure():
    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.META_PREFIX:'oai_dc', 'skip_val':55}
    encoded_invalid_token =quote(urlencode(params))
    with pytest.raises(OAIBadResumptionToken, match="Token decoding failed or format is invalid."):
        ResToken.from_token(encoded_invalid_token)

def test_invalid_token_data_types():
    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.META_PREFIX:'oai_dc', 'skip_val':datetime(2023,9,1)}
    encoded_invalid_token =quote(urlencode(params))
    with pytest.raises(OAIBadResumptionToken, match="Token decoding failed or format is invalid."):
        ResToken.from_token(encoded_invalid_token)

def test_token_decoding_random_str():
    random_str = "twinkletwinklelittlestar"
    with pytest.raises(OAIBadResumptionToken, match="Token decoding failed or format is invalid"):
        ResToken.from_token(random_str)

def test_token_decoding_with_invalid_encoding():
    with pytest.raises(OAIBadResumptionToken, match="Token decoding failed or format is invalid"):
        ResToken.from_token("?verb=ListIdentifiers&metadataPrefix=arXiv")

    with pytest.raises(OAIBadResumptionToken, match="Token decoding failed or format is invalid"):
        ResToken.from_token("")

def test_missing_key_in_token():
    params = {OAIParams.VERB: OAIVerbs.LIST_RECORDS, OAIParams.META_PREFIX:'oai_dc'}
    encoded_invalid_token =quote(urlencode(params))
    with pytest.raises(OAIBadResumptionToken, match="Token decoding failed or format is invalid."):
        ResToken.from_token(encoded_invalid_token)
