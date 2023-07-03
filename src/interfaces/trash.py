from datetime import datetime
from enum import StrEnum
from math import ceil
from uuid import uuid4
from pydantic import (BaseModel, Field, validator)  # pylint: disable=no-name-in-module


class TrashType(StrEnum):
    """
    Enumerate for the type of trash
    """
    PAPEL = 'Papel'
    VIDRIO = 'Vidrio'
    PLASTICO = 'Plastico'
    TEXTIL = 'Textil'
    ELECTRONICOS = 'Electronicos'
    BATERIAS = 'Baterias'
    ACEITE = 'Aceite'


TRASH_VALUE = {
    TrashType.PAPEL: 1.5,
    TrashType.VIDRIO: 1.2,
    TrashType.PLASTICO: 1.0,
    TrashType.TEXTIL: 0.8,
    TrashType.ELECTRONICOS: 0.7,
    TrashType.BATERIAS: 0.6,
    TrashType.ACEITE: 1.1,
}


def calculate_points(trash_type: TrashType, peso: float) -> int:
    """
    Calculate the points of a recycling operation\n
    params:
        - trash_type: TrashType. Type of trash
        - weight: float. Weight of the trash, in grams\n
    returns: 
        - int. Points associated to the operation, rounded up.
    """
    return ceil(peso * TRASH_VALUE[trash_type])

class RecycleOperation(BaseModel):
    """
    Data model for the recycling operation\n
    atributes:
        - type: TrashType. Type of trash
        - peso: float. Weight of the trash, in grams
        - container: str. Id of the container
    """
    type: TrashType = Field(description="Tipo de residuo")
    peso: float = Field(description="Peso de los residuos, en gramos", gt=0)
    container:str = Field(description="Id del contenedor", min_length=36, max_length=36)

class RecycleOperationEvent(BaseModel):
    """
    Data model for the recycling operation event\n
    atributes:
        - data: RecycleOperation. Data of the recycling operation
        - date: datetime. Timestamp of the event
    """
    data: RecycleOperation = Field(description="Data of the recycling operation")
    timestamp: datetime = Field(description="Timestamp of the event")

    @validator('timestamp')
    @classmethod
    def set_timestamp(cls, value):
        """
        Set the timestamp of the event
        """
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        if isinstance(value, float) or isinstance(value, int):
            return datetime.fromtimestamp(value)
        return value


class PointTransaction(BaseModel):
    """
    Data model for the point operation\n
    atributes:
        - value: int. Value of the operation
        - motivo: str. Reason of the operation
        - balance: int. Balance of points after the operation
        - cuid: str. Citizen unique id
    """
    cuid: str = Field(
        description="Codigo de identificaion unico del ciudadano", min_length=36, max_length=36)
    value: int = Field(description="Valor de la operación", ne=0)
    motivo: str = Field(description="Motivo de la operación")
    balance: int = Field(description="Balance actual de puntos", default=0)


class PointTransactionEvent(BaseModel):
    """
    Data model for the point operation event\n
    """
    data: PointTransaction
    timestamp: datetime = Field(description="Timestamp of the event")

    @validator('timestamp')
    @classmethod
    def set_timestamp(cls, value):
        """
        Set the timestamp of the event
        """
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        if isinstance(value, float) or isinstance(value, int):
            return datetime.fromtimestamp(value)
        return value
