

def test_schema_arXivRaw(test_client):
    response = test_client.get("/OAI/arXivRaw.xsd")
    assert response.status_code == 200
    assert b"<schema" in response.data  
    assert b"</schema>" in response.data 
    assert b'xmlns:arXivRaw="http://arxiv.org/OAI/arXivRaw/"' in response.data 
    assert b'<element name="arXivRaw" type="arXivRaw:arXivRaw_type"/>' in response.data 
    assert b'<complexType name="version_type">' in response.data 

def test_schema_arXivOld(test_client):
    response = test_client.get("/OAI/arXivOld.xsd")
    assert response.status_code == 200
    assert b"<schema" in response.data  
    assert b"</schema>" in response.data 
    assert b'xmlns:arXivOld="http://arxiv.org/OAI/arXivOld/"' in response.data 
    assert b'<element name="arXivOld" type="arXivOld:arXivOldType"/>' in response.data 
    assert b'<complexType name="arXivOldType">' in response.data 

def test_schema_arXiv(test_client):
    response = test_client.get("/OAI/arXiv.xsd")
    assert response.status_code == 200
    assert b"<schema" in response.data  
    assert b"</schema>" in response.data 
    assert b'xmlns:arXiv="http://arxiv.org/OAI/arXiv/"' in response.data 
    assert b'<element name="arXiv" type="arXiv:arXivType"/>' in response.data 
    assert b'<complexType name="authorsType">' in response.data 