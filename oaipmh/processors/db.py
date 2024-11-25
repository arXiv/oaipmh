from typing import Optional, List, Union
from sqlalchemy.orm import aliased

from arxiv.db import Session
from arxiv.db.models import Metadata
from arxiv.identifier import Identifier


def get_record_data(arxiv_id: Identifier, all_versions:bool )-> Optional[Union[Metadata, List[Metadata]]]:
    """fetch metadata for a specific paper"""
    data_subquery = (
        Session.query(Metadata)
        .filter(Metadata.paper_id == arxiv_id.id)
        .subquery()
    )

    metadata_alias = aliased(Metadata, data_subquery)
    if all_versions:
        result = Session.query(metadata_alias).all()
    else:
        result = (
            Session.query(metadata_alias)
            .filter(metadata_alias.is_current == 1)
            .first()
        )
    return result