from typing import Dict, Tuple
from datetime import datetime, timezone, timedelta
from urllib.parse import urlencode, quote, unquote, parse_qs

from oaipmh.data.oai_errors import OAIBadResumptionToken
from oaipmh.data.oai_properties import OAIParams

SKIP='skip' #a resumption token specific parameter

class ResToken:
    def __init__(self, params: Dict[OAIParams, str], start_val: int, empty=False):
        if empty:
            #to indicate the end of a resumption token sequence
            self.params = {}
            self.start_val = 0
            self.token_str = ''
            self.expires = (datetime.now(timezone.utc) + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            self.empty=True
        else:
            self.params = params
            self.start_val = start_val
            self.token_str = self.to_token()
            self.expires = (datetime.now(timezone.utc) + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            self.empty=False

    def to_token(self) -> str: 
        params = self.params.copy()
        params.pop(OAIParams.RES_TOKEN, None)
        params[SKIP]=self.start_val
        return quote(urlencode(params))

    @classmethod
    def from_token(cls, encoded_str: str) -> Tuple[Dict[str, str], int]:
        try:
            decoded_str = unquote(encoded_str)
            parsed_params = parse_qs(decoded_str)
            params = {key: value[0] for key, value in parsed_params.items()}
            if OAIParams.VERB not in params:
                raise OAIBadResumptionToken("Token structure is invalid.")
            if SKIP not in params or not params[SKIP].isdigit():
                raise OAIBadResumptionToken("Token structure is invalid.")
            start_val = int(params.pop(SKIP))
            return params, start_val
        except (Exception):
            raise OAIBadResumptionToken("Token decoding failed or format is invalid.")

