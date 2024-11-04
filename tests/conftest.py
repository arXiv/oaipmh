import pytest
from oaipmh.factory import create_web_app

TESTING_CONFIG = {
    "APPLICATION_ROOT": "",
    "TESTING": True
    }

def test_config():
    return TESTING_CONFIG.copy()

@pytest.fixture
def test_client():
    app = create_web_app(**test_config())
    with app.test_client() as client:
        yield client