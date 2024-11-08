
from oaipmh.data.oai_properties import MetadataFormat

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
    "arXiv":MetadataFormat(
        prefix="arXivRaw",
        schema="http://arxiv.org/OAI/arXivRaw.xsd",
        namespace="http://arxiv.org/OAI/arXivRaw/"
    ),
}