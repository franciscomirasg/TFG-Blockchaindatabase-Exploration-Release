from typing import Any, List, Union
from command.command import Command
from interfaces.event import ApprovalType, EventRequest
from utils.subject_factory import properties_to_object
from rich import print


class ApprovalsCommand(Command):
    """
    Command for resolving approvals
    """
    command = "approvals"
    description = "Reject or approve approvals"

    def help(self) -> str:
        """
        Help for the approvals command
        """
        return """
Command for resolving approvals
The command will show all pending approvals one by one. And will ask for a decision.
If none is provided, the approval will be skipped.
Press q to quit.
"""

    def __format_approval(self, approval: EventRequest, service) -> str:
        """
        Format approval
        """
        schema_id = approval.request.schema_id
        if schema_id is None:
            schema_id = service.get_subject(approval.request.subject_id)
            if schema_id is None:
                return "Can't parse schema_id"
            schema_id = schema_id.schema_id

        return f"""
Request:
    {properties_to_object(schema_id, approval.request.payload.json_)}
"""

    def action(self, *args, service=None, **kwargs) -> None:
        """
        Action for the approvals command
        """
        approvals: List[EventRequest] = service.get_approvals()

        if not isinstance(approvals, list):
            return approvals

        if len(approvals) == 0:
            return "No approvals found"

        print(
            f"Found {len(approvals)} approvals: (press enter for next approval, q for quit)")
        for approval in approvals:
            print(self.__format_approval(approval, service=service))
            aux = input("Approve? (y/n): ").lower()
            if aux == "":
                continue
            if aux == "q":
                return "Exiting..."
            if aux == "y" or "n":
                return service.resolve_approval(approval, ApprovalType.Accept if aux == "y" else ApprovalType.Reject)
