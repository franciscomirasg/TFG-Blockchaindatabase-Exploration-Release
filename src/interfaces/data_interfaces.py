from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, validator


class SubjectMap(BaseModel):
    """
    Container info
    """
    id: str
    subject_id: str


class SubjectMapList(BaseModel):
    """
    Container list info
    """
    last_update: Optional[str] = None
    map_list: List[SubjectMap]

    @validator("last_update", pre=True)
    @classmethod
    def date_to_str(cls, value):
        """
        Convert datetime to string
        """
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return value

    def data_to_container(self) -> str | List[str]:
        """
        Return a string or a list of strings
        """
        return [
            f"\n\t- Recycle Zone: {container.id}" for container in self.map_list
        ]

    def data_to_citizen(self) -> str | List[str]:
        """
        Return a string or a list of strings
        """
        return [
            f"\n\t- Citizen: {container.id}" for container in self.map_list
        ]

    def to_level_db(self) -> dict:
        """
        Convert model to level db compatible
        """
        return {
            "pydantic": self.__class__.__name__,
            "data": self.dict()
        }

class CitizenHost(BaseModel):
    """
    Store the host and port of a citizen. Required to send requests
    """
    last_update: str = None
    host:str
    port: int

    @validator("last_update", pre=True)
    @classmethod
    def date_to_str(cls, value):
        """
        Convert datetime to string. If value is None, set it to current time
        """
        if value is None:
            value = datetime.utcnow()
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return value

    def to_level_db(self) -> dict:
        """
        Convert model to level db compatible
        """
        return {
            "pydantic": self.__class__.__name__,
            "data": self.dict()
        }
