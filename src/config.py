from pydantic import BaseSettings #pylint: disable=missing-module-docstring


class GlobalSettings(BaseSettings):
    """
    Global settings for all clients
    """
    governance_id: str
    recycle_schema = "RecycleOperation"
    point_transaction_schema = "PointTransaction"
    citizen_schema = "Citizen"
    connection_key = "connection_data"
    self_key = "self"
    recycle_zones_key = "containers"
    citizens_key = "citizens"
    wallet_key = "wallet"
    sign_tool = "./bin/taple-sign"

    class Config: #pylint: disable=missing-class-docstring
        env_file = ".env"
        env_file_encoding = "utf-8"


global_settings = GlobalSettings()
