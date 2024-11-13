from datetime import datetime, timezone
from oaipmh.data.oai_properties import MetadataFormat

#TODO do we want to change this
EARLIEST_DATE=datetime(2007, 5, 23, 0, 0, tzinfo=timezone.utc) 

SUPPORTED_METADATA_FORMATS={
    "oai_dc":MetadataFormat(
        prefix="oai_dc",
        schema="http://www.openarchives.org/OAI/2.0/oai_dc.xsd",
        namespace="http://www.openarchives.org/OAI/2.0/oai_dc/"
    ),
    "arXiv":MetadataFormat(
        prefix="arXiv",
        schema="http://arxiv.org/OAI/arXiv.xsd",
        namespace="http://arxiv.org/OAI/arXiv/"
    ),
    "arXivOld":MetadataFormat(
        prefix="arXiv",
        schema="http://arxiv.org/OAI/arXivOld.xsd",
        namespace="http://arxiv.org/OAI/arXivOld/"
    ),
    "arXivRaw":MetadataFormat(
        prefix="arXivRaw",
        schema="http://arxiv.org/OAI/arXivRaw.xsd",
        namespace="http://arxiv.org/OAI/arXivRaw/"
    ),
}