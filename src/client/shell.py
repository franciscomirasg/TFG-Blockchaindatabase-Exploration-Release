import os
import shlex
from typing import Dict, List
from rich import print # pylint: disable=redefined-builtin
from command.command import Command
from utils.logs import log

class Shell:
    """
    Shell class that handles the user input and executes the commands
    """
    commands_map: Dict[str, Command] = {}

    def __init__(self, commands: List[Command], service):
        for command in commands:
            self.commands_map[command.command] = command
        self.service = service

    def tokenize(self, input_: str) -> List[str]:
        """
        Tokenize the input string\n
        args:
            input_: string to be tokenized
        returns:
            list of tokens
        """
        return shlex.split(input_)

    def start(self):
        """
        Start the shell
        """
        while True:
            tokens = input("> ")
            tokens = self.tokenize(tokens)
            if len(tokens) == 0:
                continue
            command = tokens[0]

            match command:
                case "exit":
                    break
                case "help":
                    self.print_help()
                    continue
                case "clear":
                    os.system("cls" if os.name == "nt" else "clear")
                    continue

            command = self.commands_map.get(command, None)
            if command is None:
                print("Unknown command")
                self.print_help()
                continue
            try:
                result = command.execute(*tokens[1:], service=self.service)
            except Exception as exception:
                print(f"Unexpected error while executing {command.command}")
                log.error(exception)
                continue
            if result:
                if isinstance(result, list):
                    for item in result:
                        print(item)
                        token = input()
                        if token != "":
                            break
                else:
                    print(result)

    def print_help(self):
        """
        Print the help for the shell
        """
        print("Available commands:")
        print("\thelp - Show this help")
        print("\tclear - Clear the screen")
        for command in self.commands_map.values():
            print(f"\t{command}")
        print("\texit - Exit the shell")
