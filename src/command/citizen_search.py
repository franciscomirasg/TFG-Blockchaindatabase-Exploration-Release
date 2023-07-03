from typing import Any, List

from rich import print

from command.command import Command
from interfaces.data_interfaces import SubjectMapList


class SearchCitizen(Command):
    """
    Search recycle zones
    """
    command = "search_citizens"
    description = "Search citizens"

    def help(self) -> str:
        """
        Help for the search recycle zones command
        """
        return """
Search and update citizens existing in the system.
This command will refresh the citizen list in the system.
Delete citizen will be removed from the system.
"""

    def __smart_output(self, containers: List[str]) -> str | List[str]:
        """
        Smart output for citizens
        """
        if len(containers) == 0:
            return "No recycle zones found"
        elif len(containers) < 5:
            return f"Found {len(containers)} recycle zones:" + "".join(containers)
        else:
            return [f"Found {len(containers)} recycle zones:"] + containers

    def action(self, *args, service=None, **kwargs) -> Any | List[Any]:
        """
        Action to search recycle zones
        """
        citizen_info: SubjectMapList = service.search_citizen()
        if not isinstance(citizen_info, SubjectMapList):
            return citizen_info
        return self.__smart_output(citizen_info.data_to_citizen())