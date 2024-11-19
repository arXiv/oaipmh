import pytest
from datetime import datetime
from arxiv.db.models import Metadata

from oaipmh.factory import create_web_app

TESTING_CONFIG = {
    "TESTING": True
    }

def test_config():
    return TESTING_CONFIG.copy()

@pytest.fixture
def test_client():
    app = create_web_app(**test_config())
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="session")
def metadata_object1():
    return Metadata(
        metadata_id=1,
        document_id=1,
        paper_id="1234.56789",
        created=datetime(2023,1,1,10,3,6),
        updated=datetime(2023,1,1,15,7,8),
        submitter_id=42,
        submitter_name="John Doe",
        submitter_email="john.doe@example.com",
        source_size=1024,
        source_format="pdf",
        source_flags=None,
        title="A Study on Dummy Objects",
        authors="John Doe, Jane Smith",
        abs_categories="cs.AI hep-lat",
        comments="Fake comments",
        proxy=None,
        report_num=None,
        msc_class=None,
        acm_class=None,
        journal_ref=None,
        doi=None,
        abstract="This is a dummy abstract for testing purposes.",
        license="arXiv License",
        version=1,
        modtime=None,
        is_current=0,
        is_withdrawn=0
    )

@pytest.fixture(scope="session")
def metadata_object2():
    return Metadata(
        metadata_id=1,
        document_id=1,
        paper_id="1234.56789",
        created=datetime(2023,2,1,10,3,6),
        updated=datetime(2023,3,1,15,7,8),
        submitter_id=42,
        submitter_name="John Doe",
        submitter_email="john.doe@example.com",
        source_size=2876,
        source_format="pdf",
        source_flags=None,
        title="A Magical Study on Dummy Objects",
        authors="John Doe, Jane Smith",
        abs_categories="cs.AI hep-lat",
        comments="Fake comments",
        proxy=None,
        report_num=None,
        msc_class=None,
        acm_class=None,
        journal_ref=None,
        doi=None,
        abstract="This is a dummy abstract for testing purposes.",
        license="arXiv License",
        version=2,
        modtime=None,
        is_current=1,
        is_withdrawn=0
    )