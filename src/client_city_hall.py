from client.client import Client
from command.citizen_search import SearchCitizen
from command.init_connection import InitConnection
from command.list_citizens import ListCitizens
from command.list_recycle import ListRecycle
from command.list_recycles_zones import ListRecycleZones
from command.search_recycle_zones import SearchRecycleZones
from command.approvals import ApprovalsCommand

client = Client("city_hall", [
    InitConnection(),
    SearchRecycleZones(),
    ListRecycleZones(),
    ListRecycle(),
    SearchCitizen(),
    ListCitizens(),
    ApprovalsCommand()
])
