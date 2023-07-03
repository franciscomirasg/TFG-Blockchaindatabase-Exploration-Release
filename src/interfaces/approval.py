
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

from interfaces.event import ApprovalType


class ApprovalResponse(BaseModel):
    """
    Approval response
    """
    approval_type: ApprovalType = Field(
        description="Approval type", alias="approvalType")

    def to_request(self):
        """
        Converts an approval response to a request.
        """
        return self.dict(by_alias=True)

    class config:  # pylint: disable=missing-class-docstring
        allow_population_by_field_name = True
