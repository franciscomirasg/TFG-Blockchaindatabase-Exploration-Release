from typing import Any, List

from pydantic import ValidationError

from command.command import Command
from interfaces.data_interfaces import CitizenHost
from interfaces.trash import RecycleOperation, TrashType
from utils.logs import log


class MakeRecycle(Command):
    """
    MakeRecycle command. Make a recycle
    """
    command = "make_recycle"
    description = "Create a recycle transaction and send it to the TAPLE node"

    def help(self) -> str:
        """
        Help for the make_recycle command
        """
        return f"""
Create a recycle transaction and send it to the TAPLE node.
The command will ask you for the amount of the recycle, weigh and types of the recycle.
You can pass the type, weigh and types of the recycle as arguments to the command.
    make_recycle <type> <weigh> <cuid>
If errors occur, the command cancel
Available types:
    {", ".join([t.value for t in TrashType])}
""".strip()

    def action(self, *args, service=None, **kwargs) -> Any | List[Any]:
        """
        Execute the make_recycle command
        """
        data_in = {
            "type": None,
            "peso": None,
            "cuid": None
        }  # Parseo inicial
        if len(args) > 0:
            try:
                data_in["type"] = TrashType(args[0])
            except ValueError:
                return f"Invalid residue type: {args[0]}"
        if len(args) > 1:
            try:
                data_in["peso"] = float(args[1])
            except ValueError:
                return f"Invalid weigh: {args[1]}, must be a number"

        if len(args) > 2:
            data_in["cuid"] = args[3]
            if len(data_in["cuid"]) != 36:
                return f"Invalid citizen id: {data_in['cuid']}, must be a uuid4"

        for key, value in data_in.items():  # Recoger datos faltantes
            if value is None:
                if key == "type":
                    print(
                        f"Available types: {', '.join([t.value for t in TrashType])}")
                data_in[key] = input(f"{key.capitalize()}: ")
                match key:
                    case "type":
                        try:
                            data_in[key] = TrashType(data_in[key])
                        except ValueError:
                            return f"Invalid residue type: {data_in[key]}"
                    case "peso":
                        try:
                            data_in[key] = float(data_in[key])
                        except ValueError:
                            return f"Invalid weigh: {data_in[key]}, must be a number"

                    case "cuid":
                        if len(data_in[key]) != 36:
                            return f"Invalid citizen id: {data_in[key]}, must be a uuid4"

        print(f"""
Readed data:
    Type: {data_in["type"]}
    Weigh: {data_in["peso"]} grams
    Citizen: {data_in["cuid"]}
""".strip())
        if input("Is this data correct? (y/n): ") != "y":
            return "Operation canceled by user"

        try:
            recycle_operation = RecycleOperation(
                container="000000000000000000000000000000000000", **data_in)
            result = service.make_recycle_opperation(recycle_operation)
            print(result)
        except ValidationError as exception:
            log.error(f"Error validating data: {exception}")
            error_string = "Encountered the following errors when validating Identidad:\n"
            for error in exception.errors():
                print(error)
                error_string += f"\tError validating: {error['loc'][0]}\n"
            return error_string

        # Try to add reward points
        print("Checking is citizen is in the system...")
        citizen = service.search_wallet(data_in["cuid"])
        if citizen is None:
            return f"Citizen with CUID: {data_in['cuid']} is not in the system. Reward points can't be added"
        location = service.get_citizen_location(data_in["cuid"])
        print(location)
        if location is None:
            print("Citizen location is not in the system. Request user node info:")
            citizen_host = {
                "host": None,
                "port": None
            }
            for key, value in citizen_host.items():
                if value is None:
                    aux = input(
                        f"{key.capitalize()} {'Default localhost' if key == 'host' else ''}: ")
                    if aux == "" and key == "host":
                        aux = "http://localhost"
                    if aux and aux != "" and aux != "q":
                        citizen_host[key] = int(aux) if key == "port" else aux
                    if aux == "q":
                        return "Location input cancelled. Abort reward"
            print(f"""
Readed data:
    Host: {citizen_host['host']}
    Port: {citizen_host['port']}
            """)
            aux = input("Is this data correct? (y/n): ")
            if aux != "y":
                return "Location input cancelled. Abort reward"
            try:
                citizen_host = CitizenHost(
                    **citizen_host
                    )
            except ValidationError as exception:
                log.warning(f"Error validating data: {exception}")
                return "Invalid connection data. Reward not added"

            service.set_citizen_location(data_in['cuid'], citizen_host)

        return service.reward_points(data_in['cuid'], recycle_operation)
