from typing import Any, List
from command.command import Command


class InitConnection(Command):
    """
    Init command. Load the connection data to the TAPLE node
    """
    command = "init"
    description = "Initialize connection to the TAPLE node"

    def help(self) -> str:
        """
        Help for the init command
        """
        return """
Initialize connection to the TAPLE node.
The command will ask you for the host, port and api key of the TAPLE node.
You can pass the host, port and api key as arguments to the command.
    init <host> <port> <api_key>
If a connection is already established, the command will ask you if you want to overwrite the existing connection.
""".strip()

    def action(self, *args, service=None, **kwargs) -> Any | List[Any]:
        """
        Execute the init command
        """
        connection = service.get_connection_data()
        if connection is None:
            connection = {
                "host": None,
                "port": None,
                "api_key": None
            }
        else:
            print(
"""
Actual connection:
    Host: {host}
    Port: {port}
    Api key: {api_key}
""".format(**connection)
            )
            response = input(
                "Do you want to overwrite the existing connection? (y/n): ").lower()
            if response == "y":
                connection = {
                    "host": None,
                    "port": None,
                    "api_key": None
                }
            else:
                return "Connection cancelled by user, existing connection not overwritten"

        if len(args) > 0:
            connection["host"] = args[0]
        if len(args) > 1:
            connection["port"] = args[1]
        if len(args) > 2:
            connection["api_key"] = args[2]

        for key, value in connection.items():
            if value is None:
                aux = input(f"{key.capitalize()} {'Default localhost' if key == 'host' else ''}: ")
                if aux == "" and key == "host":
                    aux = "http://localhost"
                if aux and aux != "" and aux != "q":
                    connection[key] = int(aux) if key == "port" else aux
                if aux == "q":
                    return "Connection cancelled by user"
        print(
"""
Readed:
    Host: {host}
    Port: {port}
    Api key: {api_key}
""".format(**connection)
        )
        response = input(
            "Do you want to initialize the connection with this data? (y/n): ").lower()
        if response == "y":
            service.set_connection_data(connection)
            return "Connection initialized"
        return "Connection cancelled by user"
