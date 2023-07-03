import json
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, validator  # pylint: disable=no-name-in-module


class ContentSignature(BaseModel):
    """
    Defines the data used to generate the signature, as well as the signer's identifier.
    """
    event_content_hash: str = Field(
        description="Hash of the event content. It's also the request id")
    signer: str = Field(description="Identifier of the signer")
    timestamp: int = Field(description="Timestamp of the event")


class Signature(BaseModel):
    """
    The format, in addition to the signature, includes additional information,
    namely the signer's identifier, the signature timestamp and the hash of the signed contents.
    """
    content: ContentSignature = Field(description="The signed content")
    signature: str = Field(description="The signature value")


class Metadata(BaseModel):
    """
    Metadata of a TAPLE Event
    """
    governance_id: str = Field(description="Identifier of the governance")
    governance_version: int = Field(
        description="Version of the governance")
    namespace: str = Field(description="Namespace")
    owner: str = Field(description="Owner identifier")
    schema_id: str = Field(description="Identifier of the schema")


class ApprovalType(str, Enum):
    """
    Approval type
    """
    Accept = "Accept"
    Reject = "Reject"


class ContentApproval(BaseModel):
    """
    Defines the data used to generate the signature, 
    as well as the signer's identifier.
    """
    approval_type: ApprovalType = Field(description="Type of approval")
    event_request_hash: str = Field(
        description="Hash of the event request")
    expected_sn: int = Field(description="Expected sequence number")
    signer: str = Field(description="Identifier of the signer")
    timestamp: int = Field(description="Timestamp of the approval")


class Approval(BaseModel):
    """
    Approval of a TAPLE Event
    """
    content: ContentApproval = Field(
        description="Content approval")
    signature: str = Field(description="The signature value")


class Payload(BaseModel):
    """
    Payload of a TAPLE Event type json
    """
    json_: Optional[dict] = Field(
        description="Payload", alias="Json", default=None)
    json_patch: Optional[dict] = Field(
        description="Payload", alias="JsonPatch", default=None)

    @validator("json_", pre=True)
    @classmethod
    def coerce_dict(cls, value):
        """
        Coerce dict
        """
        if isinstance(value, dict):
            return value
        return json.loads(value)
    
    @validator("json_patch", pre=True)
    @classmethod
    def coerce_dict_patch(cls, value):
        """
        Coerce dict
        """
        if isinstance(value, dict):
            return value
        return json.loads(value)

    class Config:  # pylint: disable=missing-class-docstring
        allow_population_by_field_name = True


class Create(BaseModel):
    """
    Create event
    """
    governance_id: str = Field(description="Governance identifier")
    namespace: str = Field(description="Namespace")
    payload: Payload = Field(description="Payload object")
    schema_id: str = Field(
        description="Identifier of the schema used by the object")


class State(BaseModel):
    """
    Change State event
    """
    payload: Payload = Field(description="Payload object")
    subject_id: str = Field(description="Subject identifier")


class RequestType(str, Enum):
    """
    Approval type
    """
    CREATE = "Create"
    STATE = "State"


class Request(BaseModel):
    """
    Request of an event
    """
    create: Optional[Create] = Field(
        description="Create event", alias="Create", default=None)
    state: Optional[State] = Field(
        description="State event", alias="State", default=None)

    @property
    def get_type(self) -> RequestType:
        """
        Get type of event
        """
        return RequestType.CREATE if self.create else RequestType.STATE
    
    @property
    def payload(self) -> Payload:
        """
        Get payload of event
        """
        return self.create.payload if self.create else self.state.payload
    
    @property
    def subject_id(self) -> str:
        """
        Get subject id of event
        """
        return self.state.subject_id if self.state else None
    
    @property
    def schema_id(self) -> str:
        """
        Get schema id of event
        """
        return self.create.schema_id if self.create else None

    class Config:  # pylint: disable=missing-class-docstring
        allow_population_by_field_name = True


class EventRequest(BaseModel):
    """
    Request that originated the event. It contains basically the proposed change and the votes obtained related to it.
    """
    approvals: List[Approval] = Field(description="List of approvals")
    request: Request = Field(description="Request object")
    signature: Signature = Field(description="Signature object")
    timestamp: int = Field(description="Timestamp")

    @property
    def request_id(self) -> str:
        """
        Get request id
        """
        return self.signature.content.event_content_hash


class EventContent(BaseModel):
    """
    Content of a TAPLE Event
    """
    approved: bool = Field(
        description="Indicates if the event is approved")
    event_request: EventRequest = Field(
        description="Request that originated the event")
    metadata: Metadata = Field(description="Metadata of the event")
    previous_hash: str = Field(description="Hash of the previous event")
    sn: int = Field(description="Sequence number of the event")
    state_hash: str = Field(description="Hash of the state")
    subject_id: str = Field(description="Subject identifier")


class Event(BaseModel):
    """
    TAPLE Event
    """
    event_content: EventContent = Field(
        description="Content of the event")
    signature: Signature = Field(description="Signature of the event")
