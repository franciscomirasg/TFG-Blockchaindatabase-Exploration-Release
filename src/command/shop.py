from typing import Any, List

from rich import print

from command.command import Command
from static.shop import ITEMS


class ShopCommand(Command):
    """
    Command for shop
    """
    command = "shop"
    description = "View and get rewards from shop"
    
    def help(self) -> str:
        return """
Shop command
Allows you to view and get rewards from shop
    shop [options]
Options:
    view: view the shop
    buy: buy a reward from the shop
If no option is provided, the command will default to view
        """
    
    def action(self, *args, service=None, **kwargs) -> Any | List[Any]:
        """
        Execute the shop command
        """
        mode = "view"
        
        if len(args) > 0:
            mode = args[0].lower()
        
        match mode:
            case "view":
                self.__print_shop()

            case "buy":
                self.__print_shop()
                item = input("Which item do you want to buy?\nPress q for exit, enter index: ")
                if item == "q":
                    return "Exiting shop"
                try:
                    item = int(item)
                except ValueError:
                    return "Invalid input"

                if item < 0 or item >= len(ITEMS):
                    return "Index out of range"
                return service.buy_item(ITEMS[item])
            case _:
                return "Invalid option. Use help for more information"

    def __print_shop(self):
        print("Welcome to the shop\nThese are the items you can redeem:")
        for idx, item in enumerate(ITEMS):
            print(f"\t{idx}. -> {item}")