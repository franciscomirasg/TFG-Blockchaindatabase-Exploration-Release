from typing import Any, List

from rich import print

from command.command import Command
from interfaces.data_interfaces import SubjectMapList


class ListRecycleZones(Command):
    """
    List recycle zones
    """
    command = "list_zones"
    description = "List recycles zones"

    def help(self) -> str:
        """
        Help for the list recycle zones command
        """
        return """
List recycle zones active in the system.
Zones maybe be not updated.
Update with the search command.
"""

    def __smart_output(self, containers: List[str], last:str) -> str | List[str]:
        """
        Smart output for recycle zones
        """
        if len(containers) == 0:
            return f"No recycle zones found. Last search: {last}"
        elif len(containers) < 5:
            return f"Last Update: {last}\nFound {len(containers)} recycle zones:" + "".join(containers)
        else:
            return [f"Last Update: {last}\nFound {len(containers)} recycle zones: (press Enter continue listing)"] + containers

    def action(self, *args, service=None, **kwargs) -> Any | List[Any]:
        """
        Action to list recycle zones
        """
        container_info: SubjectMapList = service.list_containers()
        return self.__smart_output(container_info.data_to_container(), container_info.last_update)