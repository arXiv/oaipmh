import pytest

from arxiv.identifier import Identifier

from oaipmh.data.oai_errors import OAINonexistentID
from oaipmh.requests.param_processing import process_identifier, create_oai_id

def test_process_old_id():
    expected= Identifier("cs/0007002")
    result=process_identifier("oai:arXiv.org:cs/0007002")
    assert result==expected

def test_process_new_id():
    expected= Identifier("2307.10651")
    result=process_identifier("oai:arXiv.org:2307.10651")
    assert result==expected

def test_process_bad_id():
    with pytest.raises(OAINonexistentID):
        process_identifier("cs/0007002")

    with pytest.raises(OAINonexistentID):
        process_identifier("oai:arXiv.org:cs/0007.002")

    with pytest.raises(OAINonexistentID):
        process_identifier("oai:arXiv.org:99.9999")

    with pytest.raises(OAINonexistentID):
        process_identifier("oai:arXiv.org:totally_an_id//sdfkj34o")