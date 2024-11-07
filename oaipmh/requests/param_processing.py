

from arxiv.identifier import Identifier, IdentifierException

from oaipmh.data.oai_errors import OAINonexistentID

ID_PREFIX="oai:arXiv.org:"
def process_identifier(id_str:str) -> Identifier:
    """transform an OAI identifier into an arxiv ID"""
    if not id_str.startswith(ID_PREFIX):
        raise OAINonexistentID
    
    short_id = id_str[len(ID_PREFIX):]
    try:
        arxiv_id=Identifier(short_id)
    except IdentifierException:
        raise OAINonexistentID
    
    return arxiv_id

def create_oai_id(arxiv_id: Identifier) -> str:
    #turns arxiv style id into oai style id
    return f"{ID_PREFIX}{arxiv_id.id}"