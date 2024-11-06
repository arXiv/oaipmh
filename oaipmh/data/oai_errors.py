
class OAIException(Exception):
    """General class for all OAI defined errors"""
    code: str
    description: str
    pass

class OAIBadArgument(OAIException):
    #dont include attributes
    code="badArgument"
    description="The request includes illegal arguments, is missing required arguments, includes a repeated argument, or values for arguments have an illegal syntax."
    
class OAIBadResumptionToken(OAIException):
    #TODO consider including params
    code="badResumptionToken"
    description="The value of the resumptionToken argument is invalid or expired."

class OAIBadVerb(OAIException):
    #dont include attributes
    code="badVerb"
    description="Value of the verb argument is not a legal OAI-PMH verb, the verb argument is missing, or the verb argument is repeated."

class OAIBadFormat(OAIException):
    #TODO consider including params
    code="cannotDisseminateFormat"
    description="The metadata format identified by the value given for the metadataPrefix argument is not supported by the item or by the repository."

class OAINonexistentID(OAIException):
    #TODO consider including params
    code="idDoesNotExist"
    description="The value of the identifier argument is unknown or illegal in this repository."

class OAINoRecordsMatch(OAIException):
    #TODO params
    code="noRecordsMatch"
    description="The combination of the values of the from, until, set and metadataPrefix arguments results in an empty list."

class OAINoMetadataFormats(OAIException):
    #TODO consider including params
    code="noMetadataFormats"
    description="There are no metadata formats available for the specified item."

class OAINoSetHierarchy(OAIException):
    #should not be triggered for arXiv implementation
    code="noSetHierarchy"
    description="The repository does not support sets. This exception should not be true for the arXiv implementation."