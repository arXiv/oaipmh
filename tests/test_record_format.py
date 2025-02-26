
from oaipmh.data.oai_properties import OAIParams, OAIVerbs

def test_header_format(test_client):
    params = {OAIParams.VERB: OAIVerbs.GET_RECORD, OAIParams.ID: "oai:arXiv.org:0806.4129",  OAIParams.META_PREFIX: "oai_dc"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert "<identifier>oai:arXiv.org:0806.4129</identifier>" in text
    assert '<datestamp>2014-12-15</datestamp>' in text
    assert '<setSpec>physics:math-ph</setSpec>' in text
    assert '<setSpec>math:math:MP</setSpec>' in text

def test_oai_dc_format(test_client):
    params = {OAIParams.VERB: OAIVerbs.GET_RECORD, OAIParams.ID: "oai:arXiv.org:0806.4129",  OAIParams.META_PREFIX: "oai_dc"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert '<oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ https://www.openarchives.org/OAI/2.0/oai_dc.xsd">' in text
    assert '<dc:title>Gauge Fixing in the Maxwell Like Gravitational Theory in Minkowski Spacetime and in the Equivalent Lorentzian Spacetime</dc:title>' in text
    assert '<dc:creator>Rodrigues Jr, Waldyr A.</dc:creator>' in text
    assert '<dc:creator>da Rocha, Roldao</dc:creator>' in text
    assert '<dc:subject>Mathematical Physics</dc:subject>' in text
    assert text.count('<dc:subject>Mathematical Physics</dc:subject>') == 1 #no duplicate for alias
    assert '<dc:subject>15A66</dc:subject>' in text
    assert '<dc:description>In a previous paper we investigate a Lagrangian field theory for the gravitational field' in text
    assert '<dc:description>15 pages. This version corrects some misprints of the published version</dc:description>' in text
    assert '<dc:date>2008-06-25</dc:date>' in text #initial publish day
    assert '<dc:date>2014-12-12</dc:date>' in text #publish date of latest version
    assert '<dc:type>text</dc:type>' in text #we are alwasy text
    assert '<dc:identifier>http://arxiv.org/abs/0806.4129</dc:identifier>' in text
    assert '<dc:identifier>AIP Conf.Proc.1316:466-477,2010</dc:identifier>' in text
    assert '<dc:identifier>doi:10.1063/1.3536454</dc:identifier>' in text

def test_arXivOld_format(test_client):
    params = {OAIParams.VERB: OAIVerbs.GET_RECORD, OAIParams.ID: "oai:arXiv.org:0806.4129",  OAIParams.META_PREFIX: "arXivOld"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert '<arXivOld xmlns="http://arxiv.org/OAI/arXivOld/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://arxiv.org/OAI/arXivOld/ https://oaipmh.arxiv.org/OAI/arXivOld.xsd">' in text
    assert '<id>0806.4129</id>' in text
    assert '<title>Gauge Fixing in the Maxwell Like Gravitational Theory in Minkowski Spacetime and in the Equivalent Lorentzian Spacetime</title>' in text
    assert '<authors>Roldao da Rocha, Waldyr A. Rodrigues Jr</authors>' in text
    assert '<categories>math-ph math.MP</categories>' in text
    assert '<comments>15 pages. This version corrects some misprints of the published version</comments>' in text
    assert '<msc-class>15A66</msc-class>' in text
    assert '<acm-class>' not in text
    assert '<journal-ref>AIP Conf.Proc.1316:466-477,2010</journal-ref>' in text
    assert '<doi>10.1063/1.3536454</doi>' in text
    assert '<license>http://arxiv.org/licenses/nonexclusive-distrib/1.0/</license>' in text
    assert '<abstract>In a previous paper we investigate a Lagrangian field' in text

def test_arXiv_format(test_client):
    params = {OAIParams.VERB: OAIVerbs.GET_RECORD, OAIParams.ID: "oai:arXiv.org:0806.4129",  OAIParams.META_PREFIX: "arXiv"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert '<arXiv xmlns="http://arxiv.org/OAI/arXiv/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://arxiv.org/OAI/arXiv/ https://oaipmh.arxiv.org/OAI/arXiv.xsd">' in text
    assert '<id>0806.4129</id>' in text
    assert '<title>Gauge Fixing in the Maxwell Like Gravitational Theory in Minkowski Spacetime and in the Equivalent Lorentzian Spacetime</title>' in text
    assert '<keyname>da Rocha</keyname>' in text
    assert '<forenames>Roldao</forenames>' in text
    assert '<suffix>Jr</suffix>' in text
    assert '<categories>math-ph math.MP</categories>' in text
    assert '<comments>15 pages. This version corrects some misprints of the published version</comments>' in text
    assert '<msc-class>15A66</msc-class>' in text
    assert '<acm-class>' not in text
    assert '<journal-ref>AIP Conf.Proc.1316:466-477,2010</journal-ref>' in text
    assert '<doi>10.1063/1.3536454</doi>' in text
    assert '<license>http://arxiv.org/licenses/nonexclusive-distrib/1.0/</license>' in text
    assert '<abstract>In a previous paper we investigate a Lagrangian field' in text

def test_arXivRaw_format(test_client):
    params = {OAIParams.VERB: OAIVerbs.GET_RECORD, OAIParams.ID: "oai:arXiv.org:0806.4129",  OAIParams.META_PREFIX: "arXivRaw"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert '<arXivRaw xmlns="http://arxiv.org/OAI/arXivRaw/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://arxiv.org/OAI/arXivRaw/ https://oaipmh.arxiv.org/OAI/arXivRaw.xsd">' in text
    assert '<id>0806.4129</id>' in text
    assert '<title>Gauge Fixing in the Maxwell Like Gravitational Theory in Minkowski Spacetime and in the Equivalent Lorentzian Spacetime</title>' in text
    assert '<authors>Roldao da Rocha, Waldyr A. Rodrigues Jr</authors>' in text
    assert '<categories>math-ph math.MP</categories>' in text
    assert '<comments>15 pages. This version corrects some misprints of the published version</comments>' in text
    assert '<msc-class>15A66</msc-class>' in text
    assert '<acm-class>' not in text
    assert '<journal-ref>AIP Conf.Proc.1316:466-477,2010</journal-ref>' in text
    assert '<doi>10.1063/1.3536454</doi>' in text
    assert '<license>http://arxiv.org/licenses/nonexclusive-distrib/1.0/</license>' in text
    assert '<abstract>In a previous paper we investigate a Lagrangian field' in text
    assert '<version version="v1">' in text
    assert '<date>Wed, 25 Jun 2008 15:29:38 GMT</date>' in text
    assert '<size>14kb</size>' in text
    assert '<version version="v2">' in text
    assert '<version version="v3">' in text
    assert '<version version="v4">' in text
    assert '<version version="v5">' in text
    assert '<version version="v6">' in text
    assert '<date>Tue, 15 Sep 2009 17:34:26 GMT</date>' in text
    assert '<date>Fri, 12 Dec 2014 13:15:28 GMT</date>' in text
    assert '<size>17kb</size>' in text

    #source flags
    params = {OAIParams.VERB: OAIVerbs.GET_RECORD, OAIParams.ID: "oai:arXiv.org:1001.3172",  OAIParams.META_PREFIX: "arXivRaw"}
    response = test_client.get("/oai", query_string=params)
    assert response.status_code == 200 
    text=response.get_data(as_text=True)
    assert '<source_type>D</source_type>' in text



