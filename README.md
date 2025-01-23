# arxiv_oaipmh
handles requests to the OAI PMH service which provides metadata on arXiv papers.
The main specifications can be found here: https://www.openarchives.org/OAI/2.0/openarchivesprotocol.htm 
and a simpler arXiv specific description of how to use the service can be found here: https://info.arxiv.org/help/oa/index.html

# run locally
install dependencies:
poetry install

run:
python main.py

Then check the app is running with http://localhost:8080/oai?verb=Identify

to run off of the main arXiv database:
export CLASSIC_DB_URI="SECRET_HERE"

tests:
pytest tests