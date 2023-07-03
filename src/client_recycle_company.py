from command.init_connection import InitConnection
from client.client import Client
from command.search_recycle_zones import SearchRecycleZones
from command.list_recycles_zones import ListRecycleZones
from command.list_recycle import ListRecycle

client = Client("recicle_company", [
    InitConnection(),
    SearchRecycleZones(),
    ListRecycleZones(),
    ListRecycle()
])
