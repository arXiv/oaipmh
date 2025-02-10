
class OAIParams:
    VERB = "verb"
    ID = "identifier"
    META_PREFIX = "metadataPrefix"
    SET = "set"
    FROM = "from"
    UNTIL = "until"
    RES_TOKEN = "resumptionToken"

class OAIVerbs:
    GET_RECORD = "GetRecord"
    LIST_RECORDS = "ListRecords"
    LIST_IDS = "ListIdentifiers"
    IDENTIFY = "Identify"
    LIST_META_FORMATS = "ListMetadataFormats"
    LIST_SETS = "ListSets"

class MetadataFormat:
    def __init__(self, prefix: str, schema: str, namespace: str, all_versions:bool):
        self.prefix = prefix
        self.schema = schema
        self.namespace = namespace
        self.all_versions= all_versions

