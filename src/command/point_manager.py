from typing import Any, List, Union
from command.command import Command
from interfaces.trash import PointTransaction, PointTransactionEvent

class PointManager(Command):
    """
    Command for managing point wallet of the citizen
    """

    command = "points"
    description = "Manage point wallets"

    def help(self) -> str:
        """
        Help for the point command
        """
        return """
Manage your point wallet.
You can view your current points and historial if not wallet is created, the command will create a new one.
    points [options]
    Options:
        view: view your point wallet
        history: view the history of your point wallet
If no option is provided, the command will default to view
"""

    def __format_wallet(self, wallet: PointTransaction) -> str:
        """
        Format the wallet for printing
        """
        return f"""
Your wallet:
    Point Balance: {wallet.balance}
        """

    def __format_wallet_history(self, wallet: PointTransaction, history: List[PointTransactionEvent]) -> List[str]:
        results = [
            f"Your wallet:\n\tPoint Balance: {wallet.balance}\nFound {len(history)} transactions\nPress enter to continue, q to quit",
        ]
        for event in history:
            results.append(f"""
Transaction at: {event.timestamp}
    Value: {event.data.value}
    Motive: {event.data.motivo}
    Point Balance: {event.data.balance}\n
""")
        results.append("End of listed transactions")
        return results

    def action(self, *args, service=None, **kwargs) -> Any | List[Any]:
        """
        Execute the point wallet
        """
        mode = "view"

        if len(args) > 0:
            mode = args[0].lower()

        wallet = service.init_wallet()
        if wallet is None:
            return "Your client does not have a citizen created. Please use citizen command to create one."
        if isinstance(wallet,str):
            return wallet

        match mode:
            case "view":
                return self.__format_wallet(wallet)
            case "history":
                history = service.get_wallet_history()
                if isinstance(history,str):
                    return history
                return self.__format_wallet_history(wallet, history)
