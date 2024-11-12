from datetime import datetime, timezone
from typing import Dict, Any, Union

from flask import render_template

from arxiv.taxonomy.category import Group, Archive, Category
from arxiv.taxonomy.definitions import ARCHIVES_ACTIVE

from oaipmh.data.oai_properties import OAIParams
from oaipmh.serializers.output_formats import Response

def produce_set_list(query_data: Dict[OAIParams, Any]) -> Response:
    """create the set structure of a repository"""
    #TODO display in desired form/ level of depth once decided
    #TODO filter out hidden entries
    response=render_template("setSpec.xml", 
                response_date=datetime.now(timezone.utc),
                query_data=query_data,
                archives=ARCHIVES_ACTIVE)
    return response, 200, {}

def make_set_str(item: Union[Group, Archive, Category]) -> str:
    """helper function to convert arXiv category data into OAI set structure
    the grp_ prefix should be removed from group ids
    """
    if isinstance(item, Group):
        return item.id[4:]
    elif isinstance(item, Archive):
        return f"{item.in_group[4:]}:{item.id}"
    elif isinstance(item, Category):
        archive=item.get_archive()
        return f"{archive.in_group[4:]}:{item.id.replace('.',':')}"
