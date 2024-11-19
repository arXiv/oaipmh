from typing import Optional, List

from arxiv.db import Session
from arxiv.db.models import Metadata
from arxiv.identifier import Identifier


def get_record_data_current(arxiv_id: Identifier )-> Optional[Metadata]:
    """fetch latest metadata for a specific paper"""
    data=(Session.query(Metadata)
          .filter(Metadata.paper_id == arxiv_id.id)
          .filter(Metadata.is_current==1)
          .first()
    )
    return data
    
def get_record_data_all(arxiv_id: Identifier)-> Optional[List[Metadata]]:
    """fetch all metadata for a specific paper"""
    data=(Session.query(Metadata)
          .filter(Metadata.paper_id == arxiv_id.id)
          .all()
    )
    return data