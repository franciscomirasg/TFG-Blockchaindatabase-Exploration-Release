from enum import Enum
import json
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator  # pylint: disable=no-name-in-module

# Subject


class Subject(BaseModel):
    """Subject model"""
    governance_id: str = Field(description="Governance identifier")
    namespace: str = Field(description="Namespace")
    owner: str = Field(description="Subject owner identifier")
    properties: Dict[str, Any] = Field(
        description="Current status of the subject")
    public_key: str = Field(description="Public key of the subject")
    schema_id: str = Field(
        description="Identifier of the schema used by the subject and defined in associated governance")
    sn: int = Field(description="Current sequence number of the subject")
    subject_id: str = Field(description="Subject identifier")

    @property
    def is_governance(self):
        """
        Is this subject a governance
        """
        return self.governance_id == ""
    
    @validator("properties", pre=True)
    @classmethod
    def coerce_dict(cls, value):
        """
        Coerce dict
        """
        if isinstance(value, dict):
            return value
        return json.loads(value)
