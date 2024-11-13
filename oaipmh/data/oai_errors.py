from typing import Dict, Optional

from oaipmh.data.oai_properties import OAIParams

class OAIException(Exception):
    """General class for all OAI defined errors"""
    code: str
    description: str
    query_params: Optional[Dict[OAIParams, str]]
    reason: Optional[str]

class OAIBadArgument(OAIException):
    code="badArgument"
    description="The request includes illegal arguments, is missing required arguments, includes a repeated argument, or values for arguments have an illegal syntax."
    query_params=None #dont include attributes
    def __init__(self, reason:str= None):
        self.reason=reason

class OAIBadResumptionToken(OAIException):
    code="badResumptionToken"
    description="The value of the resumptionToken argument is invalid or expired."
    def __init__(self, reason:str, query_params: Dict[OAIParams, str] = None):
        self.query_params=query_params
        self.reason=reason

class OAIBadVerb(OAIException):
    code="badVerb"
    description="Value of the verb argument is not a legal OAI-PMH verb, the verb argument is missing, or the verb argument is repeated."
    query_params=None #dont include attributes
    def __init__(self, reason:str= None):
        self.reason=reason

class OAIBadFormat(OAIException):
    code="cannotDisseminateFormat"
    description="The metadata format identified by the value given for the metadataPrefix argument is not supported by the item or by the repository."
    def __init__(self, reason:str= None, query_params: Dict[OAIParams, str] = None):
        self.query_params=query_params
        self.reason=reason

class OAINonexistentID(OAIException):
    code="idDoesNotExist"
    description="The value of the identifier argument is unknown or illegal in this repository."
    def __init__(self, reason:str= None, query_params: Dict[OAIParams, str] = None):
        self.query_params=query_params
        self.reason=reason

class OAINoRecordsMatch(OAIException):
    code="noRecordsMatch"
    description="The combination of the values of the from, until, set and metadataPrefix arguments results in an empty list."
    def __init__(self, reason:str= None, query_params: Dict[OAIParams, str] = None):
        self.query_params=query_params
        self.reason=reason

class OAINoMetadataFormats(OAIException):
    code="noMetadataFormats"
    description="There are no metadata formats available for the specified item."
    def __init__(self, reason:str= None, query_params: Dict[OAIParams, str] = None):
        self.query_params=query_params
        self.reason=reason

class OAINoSetHierarchy(OAIException):
    #should not be triggered for arXiv implementation
    code="noSetHierarchy"
    description="The repository does not support sets. This exception should not be true for the arXiv implementation."
    def __init__(self, reason:str= None, query_params: Dict[OAIParams, str] = None):
        self.query_params=query_params
        self.reason=reason