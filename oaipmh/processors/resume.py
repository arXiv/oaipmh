from typing import Dict, Tuple
import json
import base64

from oaipmh.data.oai_errors import OAIBadResumptionToken
from oaipmh.data.oai_properties import OAIParams

class ResToken:
    def __init__(self, params: Dict[OAIParams, str], start_val: int):
        self.params = params
        self.start_val = start_val
        self.token_str = self.to_token()
        #TODO expire on next announce

    def to_token(self) -> str: #TODO encode special characters
        params = self.params.copy()
        params.pop("resumptionToken", None)
        data = {
            "params": params,
            "start_val": self.start_val
        }
        json_str = json.dumps(data)
        return base64.b64encode(json_str.encode("utf-8")).decode("utf-8")

    @classmethod
    def from_token(cls, encoded_str: str) -> Tuple[Dict[str, str], int]:
        try:
            json_str = base64.b64decode(encoded_str).decode("utf-8")
            data = json.loads(json_str)
            if not isinstance(data, dict) or set(data.keys()) != {"params", "start_val"}:
                raise OAIBadResumptionToken("Token structure is invalid.")
            if not isinstance(data["params"], dict) or not isinstance(data["start_val"], int):
                raise OAIBadResumptionToken("Token contains invalid data types.")
            return data["params"], data["start_val"]
        except (Exception):
            raise OAIBadResumptionToken("Token decoding failed or format is invalid.")

