import pytest

from arxiv.identifier import Identifier

from oaipmh.data.oai_errors import OAINonexistentID
from oaipmh.requests.param_processing import process_identifier, create_oai_id

def test_process_old_id():
    paper_id="cs/0007002"
    expected= Identifier(paper_id)
    result=process_identifier(create_oai_id(paper_id))
    assert result==expected

def test_process_new_id():
    paper_id="2307.10651"
    expected= Identifier(paper_id)
    result=process_identifier(create_oai_id(paper_id))
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