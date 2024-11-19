from datetime import datetime, timezone
from oaipmh.data.oai_properties import MetadataFormat

#TODO test/ determine limits
RECORDS_LIMIT=2000
IDENTIFIERS_LIMIT=5000 

SUPPORTED_METADATA_FORMATS={
    "oai_dc":MetadataFormat(
        prefix="oai_dc",
        schema="http://www.openarchives.org/OAI/2.0/oai_dc.xsd",
        namespace="http://www.openarchives.org/OAI/2.0/oai_dc/",
        all_versions=True
    ),
    "arXiv":MetadataFormat(
        prefix="arXiv",
        schema="http://arxiv.org/OAI/arXiv.xsd",
        namespace="http://arxiv.org/OAI/arXiv/",
        all_versions=False
    ),
    "arXivOld":MetadataFormat(
        prefix="arXivOld",
        schema="http://arxiv.org/OAI/arXivOld.xsd",
        namespace="http://arxiv.org/OAI/arXivOld/",
        all_versions=False
    ),
    "arXivRaw":MetadataFormat(
        prefix="arXivRaw",
        schema="http://arxiv.org/OAI/arXivRaw.xsd",
        namespace="http://arxiv.org/OAI/arXivRaw/",
        all_versions=True
    ),
}

#required definiton
REPOSITORY_NAME='arXiv'
BASE_URL='https://arxiv.org/oai'
PROTOCOL_VERSION='2.0'
EARLIEST_DATE=datetime(2007, 5, 23, 0, 0, tzinfo=timezone.utc) #TODO change?
DELETED_RECORD='persistent'
GRANULARITY='YYYY-MM-DD'
ADMIN_EMAIL='help@arxiv.org'