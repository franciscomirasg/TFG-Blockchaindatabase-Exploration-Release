from typing import Any, List
from command.command import Command
from interfaces.data_interfaces import SubjectMapList
from interfaces.trash import RecycleOperationEvent


class ListRecycle(Command):
    """
    List recycle command
    """
    command = "list_recycle"
    description = "List recycle history for a container or all containers"

    def help(self) -> str:
        """
        Help for the list recycle command
        """
        return """
List recycle history for a container or all containers.
Usage: list_recycle [option]
if no option is provided, prompt for a container is shown.
Options:
    <container_id>: List recycle history for container with id <container_id>
    all: List recycle history for all containers
    prompt: Prompt for a container id and then list recycle history for that container
"""

    def __enumerate_containers(self, containers: SubjectMapList) -> List[str]:
        """
        Enumerate containers
        """
        string_builder = f"Last search: {containers.last_update}\n Found {len(containers.map_list)} recycle zones:"
        for index, container in enumerate(containers.map_list):
            string_builder += f"\n\t{index}: Recycle Zone {container.id}"
        return string_builder

    def __format_events(self, events: List[RecycleOperationEvent]) -> List[str]:
        """
        Format recycle events
        """
        string_builder = [
            f"Total events: {len(events)}:\n (press enter for next event, q for quit)"]
        for event in events:
            string_builder.append(
                f"Recycle operation {event.timestamp.strftime('%Y-%m-%d %H:%M:%S')}:\n\tResidue class: {event.data.type}\n\tResidue weight: {event.data.peso} grams\n\tContainer: {event.data.container}")

        string_builder.append("Listed all events")
        return string_builder

    def action(self, *args, service=None, **kwargs) -> Any | List[Any]:
        """
        Action for the list recycle command
        """
        mode = "prompt"
        if len(args) > 0:
            mode = args[0].lower() if len(args[0]) != 36 else "container"
        results: List[RecycleOperationEvent] = []

        match mode:
            case "prompt":
                containers: SubjectMapList = service.list_containers()
                if len(containers.map_list) < 1:
                    return "No citizens found"
                print(self.__enumerate_containers(containers))
                container = int(input("Container id: "))
                if container >= len(containers.map_list):
                    return "Invalid container index"
                results = service.list_recycle_by_container(
                    containers.map_list[container].id)
                if not isinstance(results, list):
                    return results
                return self.__format_events(results)
            case "container":
                results = service.list_recycle_by_container(args[0])
                if not isinstance(results, list):
                    return results
                return self.__format_events(results)
            case "all":
                results = service.list_recycle_all_containers()
                if not isinstance(results, list):
                    return results
                return self.__format_events(results)
            case _:
                return "Invalid option. Use help for more information"