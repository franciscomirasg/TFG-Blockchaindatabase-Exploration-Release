from pydantic import BaseModel  # pylint: disable=no-name-in-module

from interfaces.event import Request, RequestType, Signature


class EventOut(BaseModel):
    """
    Event request to node
    """
    request: Request
    signature: Signature = None
    timestamp: int = None

    def to_request(self) -> dict:
        """
        Convert to RestRequest
        """
        aux_dict = self.dict(by_alias=True)
        if self.request.get_type == RequestType.CREATE:
            aux_dict["request"].pop("State", None)
            aux_dict["request"]["Create"]["payload"].pop("JsonPatch", None)
        else:
            aux_dict["request"].pop("Create", None)
            aux_dict["request"]["State"]["payload"].pop("JsonPatch", None)
        return aux_dict
    
    def get_signable_payload(self) -> str:
        """
        Convert to signable request
        """
        if self.request.get_type == RequestType.CREATE:
            raise ValueError("Create request cannot be external")
        aux_dict = self.to_request()["request"]["State"]
        return aux_dict



class EventIn(BaseModel):
    """
    Event response from node
    """
    request: Request
    request_id: str
    sn: int | None
    subject_id: str
    timestamp: int
