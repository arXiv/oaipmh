from typing import Optional

from arxiv.db import Session
from arxiv.db.models import Metadata
from arxiv.identifier import Identifier

def get_record_data(arxiv_id: Identifier)-> Optional[Metadata]:
    """fetch latest metadata for a specific paper"""
    data=(Session.query(Metadata)
          .filter(Metadata.paper_id == arxiv_id.id)
          .filter(Metadata.is_current==1)
          .first()
    )
    return data
    