import re  # pylint: disable=missing-module-docstring
from enum import StrEnum
from uuid import uuid4

from pydantic import (BaseModel, Field,  # pylint: disable=no-name-in-module
                      ValidationError, validator)

_nif_pattern = re.compile(r'^[0-9]{8}[TRWAGMYFPDXBNJZSQVHLCKE]$')
_nie_pattern = re.compile(r'^[XYZ][0-9]{7}[TRWAGMYFPDXBNJZSQVHLCKE]$')
_VALID_LETTERS = 'TRWAGMYFPDXBNJZSQVHLCKET'

UPDATABLES_KEYS = ["Name", "Surname", "NI", "Address type",
                   "Address", "Postal code", "Community", "City"]


class ViaType(StrEnum):
    """
    Enumerate for the type of street
    """
    CALLE = 'Calle'
    AVENIDA = 'Avenida'
    PLAZA = 'Plaza'
    PASEO = 'Paseo'
    CARRETERA = 'Carretera'
    CAMINO = 'Camino'
    ALAMEDA = 'Alameda'
    OTRO = 'Otro'


class Identidad(BaseModel):
    """
    Data model for the identity of a citizen\n
    atributes:\n
        - nombre: str. Name
        - apellidos: str. Surnames
        - ni: str. DNI
    """
    nombre: str = Field(description="Nombre del ciudadano", alias="Name")
    apellidos: str = Field(
        description="Primer apellido del ciudadano", alias="Surname")
    ni: str = Field(description="DNI del ciudadano",
                    min_length=9, max_length=9, alias="NI")

    @staticmethod
    def __validate_dni(ni: str):
        if not _nif_pattern.fullmatch(ni) and not _nie_pattern.fullmatch(ni):
            raise ValidationError("Número de identificación invalido")
        aux = ni[0].replace('X', '0').replace(
            'Y', '1').replace('Z', '2') + ni[1:]
        letter = aux[-1]
        index = int(aux[:-1]) % 23
        if _VALID_LETTERS[index] != letter:
            raise ValidationError("Número de identificación fiscal invalido")

    @validator("ni")
    @classmethod
    def validate_ni(cls, value: str):
        """
        Validate the DNI
        """
        value = value.upper()
        cls.__validate_dni(value)
        return value

    class Config:  # pylint: disable=missing-class-docstring
        allow_population_by_field_name = True


class Direcion(BaseModel):
    """
    Data model for the address of a citizen\n
    atributes:
        - type: ViaType. Type of street
        - direccion: str. Address
        - codigo_postal: str. Postal code
        - comunidad: str. Community
        - ciudad: str. City
    """
    type: ViaType = Field(description="Tipo de vía", alias="Address type")
    direccion: str = Field(description="Direccion", alias="Address")
    codigo_postal: str = Field(
        description="Codigo Postal", max_length=5, min_length=5, alias="Postal code")
    comunidad: str = Field(
        description="Comunidad/Region/Provincia", alias="Community")
    ciudad: str = Field(description="Ciudad", alias="City")

    class Config:  # pylint: disable=missing-class-docstring
        allow_population_by_field_name = True


class Citizen(BaseModel):
    """
    Data model for the citizen\n
    atributes:
        - identidad: Identidad. Identity of the citizen
        - direccion: Direcion. Address of the citizen
        - cuid: str. Unique identification code of the citizen
    """
    identidad: Identidad = Field(description="Identidad del ciudadano")
    direccion: Direcion = Field(description="Direcion del ciudadano")
    cuid: str = Field(
        description="Codigo de identificaion unico del ciudadano", min_length=36, max_length=36,
        default_factory=lambda: str(uuid4()))

    class Config:  # pylint: disable=missing-class-docstring
        allow_population_by_field_name = True
