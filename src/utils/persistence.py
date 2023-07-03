from pathlib import Path
import leveldb  # pylint: disable=no-name-in-module
from typing import Dict
import json
import os
from pydantic import BaseModel
from utils.subject_factory import dict_to_model


class Persistence:
    """
    Persistence class for storing data in leveldb
    """

    def __init__(self, db_path):
        """
        :param db_path: path to the leveldb database
        """
        self.db_path = db_path
        self.__make_to_path(self.db_path)
        self.db = leveldb.LevelDB(self.db_path, create_if_missing=True)

    @staticmethod
    def __make_to_path(path:str):
        """
        Make a path to a file
        """
        full_path = Path(path)
        full_path.parent.mkdir(parents=True, exist_ok=True)

    def get(self, key: str) -> Dict|BaseModel|None:
        """
        Get value from leveldb
        """
        key = key.encode("utf-8")
        try:
            result =  self.db.Get(key)
            result = result.decode("utf-8")
            result = json.loads(result)
            if "pydantic" in result:
                return dict_to_model(result["pydantic"], result["data"])
            return result
        except KeyError:
            return None

    def put(self, key: str, value: Dict|BaseModel) -> None:
        """
        Put value in leveldb
        """
        key = key.encode("utf-8")
        if isinstance(value, BaseModel):
            value = value.to_level_db()
        value = json.dumps(value).encode("utf-8")
        self.db.Put(key, value)

    def delete(self, key: str) -> None:
        """
        Delete value from leveldb
        """
        key = key.encode("utf-8")
        self.db.Delete(key)
