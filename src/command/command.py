from abc import ABC, abstractmethod
from typing import Any, List, Union
from utils.logs import log


class Command(ABC):
    """
    Abstract class for all commands
    attributes:
        command: str - command name
    """
    command: str
    description: str

    def execute(self, *args, service=None, **kwargs) -> Any | List[Any]:
        """
        Execute the command
        """
        if len(args) > 0 and args[0] == "help":
            return self.help()
        if service is None:
            log.error("No service provided")
            raise ValueError("No service provided")
        return self.action(*args, service=service, **kwargs)

    @abstractmethod
    def action(self, *args, service=None, **kwargs) -> Union[Any, List[Any]]:
        """
        Abstract method for defining the action
        """

    def __str__(self):
        return f"{self.command}: {self.description}"

    @abstractmethod
    def help(self) -> str:
        """
        Abstract method for getting help
        """
        pass
