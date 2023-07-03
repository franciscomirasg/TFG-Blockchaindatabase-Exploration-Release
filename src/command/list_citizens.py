from typing import Any, List

from rich import print

from command.command import Command
from interfaces.citizen import Citizen
from interfaces.data_interfaces import SubjectMapList


class ListCitizens(Command):
    """
    List recycle command
    """
    command = "list_citizens"
    description = "View citizens in the system"

    def help(self) -> str:
        """
        Help for the list recycle command
        """
        return """
View citizens in the system.
Can view all citizens or a specific citizen.
Usage: list_citizens [option]
Options:
    <cuid>: Show citizen info for citizen with <cuid>
    all: Show all citizens
    prompt: Prompt for a citizen and then show citizen info for that citizen
If not option is provided, prompt will be used.
"""

    def __enumerate_citizens(self, citizens: SubjectMapList) -> List[str]:
        """
        Enumerate containers
        """
        string_builder = f"Last search: {citizens.last_update}\n Found {len(citizens.map_list)} recycle zones:"
        for index, container in enumerate(citizens.map_list):
            string_builder += f"\n\t{index}: Citizen: {container.id}"
        return string_builder

    def __format_citizen(self, events: Citizen) -> str:
        """
        Format citizens
        """
        return f"""
Citizen: 
    CUID: {events.cuid}
    NI: {events.identidad.ni}
    Name: {events.identidad.nombre}
    Surname: {events.identidad.apellidos}
    Address:
        {events.direccion.type} {events.direccion.direccion}
        Postal Code: {events.direccion.codigo_postal}
        City: {events.direccion.ciudad}
        Province: {events.direccion.comunidad}
"""
    
    def __format_list(self, events: List[Citizen]) -> List [str]:
        """
        Format citizens
        """
        result = [f"Found {len(events)} citizens: (press enter for next event, q for quit)"]
        for event in events:
            result.append(self.__format_citizen(event))
        result.append("Listed all citizens")


        return result

    def action(self, *args, service=None, **kwargs) -> Any | List[Any]:
        """
        Action for the list recycle command
        """
        mode = "prompt"
        if len(args) > 0:
            mode = args[0].lower() if len(args[0]) != 36 else "cuid"

        result = None

        match mode:
            case "prompt":
                containers: SubjectMapList = service.list_citizen()
                if len(containers.map_list) < 1:
                    return "No citizens found"
                print(self.__enumerate_citizens(containers))
                container = input("Container id: ")
                try:
                    container = int(container)
                except ValueError:
                    return "Invalid container index"

                if container >= len(containers.map_list) and container < 0:
                    return "Invalid container index"

                result = service.get_citizen_by_id(
                    containers.map_list[container].id)

                if not isinstance(result, Citizen):
                    return result
                return self.__format_citizen(result)

            case "cuid":
                result = service.get_citizen_by_id(args[0])
                if not isinstance(result, Citizen):
                    return result
                return self.__format_citizen(result)

            case "all":
                result = service.list_all_citizens()
                if not isinstance(result, list):
                    return result
                return self.__format_list(result)

            case _:
                return "Invalid option. Use help for more information"
