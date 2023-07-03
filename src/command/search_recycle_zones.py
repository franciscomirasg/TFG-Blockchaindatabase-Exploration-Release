from typing import Any, List
from command.command import Command
from interfaces.data_interfaces import SubjectMapList

class SearchRecycleZones(Command):
    """
    Search recycle zones
    """
    command = "search_zones"
    description = "Search recycles zones"

    def help(self) -> str:
        """
        Help for the search recycle zones command
        """
        return """
Search and update recycle zones active in the system.
This command will refresh the recycle zones list in the system.
Delete recycle zones will be removed from the system.
"""

    def __smart_output(self, containers: List[str]) -> str | List[str]:
        """
        Smart output for recycle zones
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
        container_info: SubjectMapList = service.search_containers(
        )
        if not isinstance(container_info, SubjectMapList):
            return container_info
        return self.__smart_output(container_info.data_to_container())
