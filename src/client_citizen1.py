from client.client import Client
from command.citizen_info import CitizenInfo
from command.init_connection import InitConnection
from command.point_manager import PointManager
from command.shop import ShopCommand

client = Client("citizen1", [
    InitConnection(),
    CitizenInfo(),
    PointManager(),
    ShopCommand()
])
