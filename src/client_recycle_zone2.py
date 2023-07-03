from command.init_connection import InitConnection
from command.make_recycle import MakeRecycle
from client.client import Client

client = Client("recicle_zone_2", [
    InitConnection(),
    MakeRecycle()
])
