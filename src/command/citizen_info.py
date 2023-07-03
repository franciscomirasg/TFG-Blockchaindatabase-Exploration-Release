from typing import Any, List

from pydantic import ValidationError

from command.command import Command
from interfaces.citizen import Citizen, Direcion, Identidad, ViaType, UPDATABLES_KEYS
from utils.logs import log


class CitizenInfo(Command):
    """
    Command for managing the citizen info
    """

    command = "citizen"
    description = "Manage citizen info"

    def help(self) -> str:
        """
        Help for the citizen command
        """
        return """
Create, view or update your digital identity.
If you are a new citizen, the command will create a new digital identity.
The city hall shall verify your identity or approve changes.
    citizen [options]
Options:
    view: view your digital identity
    update: update your digital identity
If no option is passed, the command show your digital identity
"""

    def __format_citizen(self, citizen: Citizen) -> str:
        """
        Format citizen info
        """
        return f"""
Citizen:
    Name: {citizen.identidad.nombre}
    Surname: {citizen.identidad.apellidos}
    NI: {citizen.identidad.ni}
    CUID: {citizen.cuid}
    Address:
        Type: {citizen.direccion.type.value}
        Address: {citizen.direccion.direccion}
        Postal code: {citizen.direccion.codigo_postal}
        Community: {citizen.direccion.comunidad}
        City: {citizen.direccion.ciudad}
"""

    def action(self, *args, service=None, **kwargs) -> Any | List[Any]:
        """
        Execute the citizen command
        """
        mode = "view"
        if len(args) > 0:
            mode = args[0].lower()

        citizen: Citizen = service.get_citizen_info()

        if isinstance(citizen, str):
            return citizen

        if citizen is None:
            mode = "create"

        match mode:
            case "view":
                return self.__format_citizen(citizen)

            case "update":
                changes = False
                print("Retype values to update. Leave blank to keep the current value\nPress q to quit")
                for updatable_key in UPDATABLES_KEYS:
                    old = self.__get_old_by_key(citizen, updatable_key)
                    new = input(f"{updatable_key} ({old}): ")

                    if new == "q":
                        return "Update aborted by user"
                    if old == new or new == "":
                        continue
                    if len(new) < 2:
                        return f"Invalid value for {updatable_key}"
                    if updatable_key == "Postal code" and len(new) != 5:
                        return f"Invalid value for {updatable_key}. Must be 5 digits"
                    if updatable_key == "Address type":
                        try:
                            new = ViaType(new)
                        except ValueError:
                            return f"Invalid adress type: {new}"
                    
                    changes = True
                    self.__update_citizen_by_key(citizen, updatable_key, new)

                if not changes:
                    return "No changes detected. Update aborted"
                print("Readed new citizen info: ")
                print(self.__format_citizen(citizen))
                aux = input("Is this info correct? (y/n): ")
                if aux.lower() == "y":
                    return service.update_citizen(citizen)
                else:
                    return "Update aborted by user"

            case "create":
                print("Creating new citizen. Please enter the following information:")
                identidad = {
                    "Name": None,
                    "Surname": None,
                    "NI": None
                }
                for key in identidad:
                    aux = input(f"{key}: ")
                    if len(aux) < 2:
                        return f"Invalid value for {key.capitalize()}"
                    identidad[key] = aux
                try:
                    identidad = Identidad(**identidad)
                except ValidationError as error:
                    log.error(error)
                    error_string = "Encountered the following errors when validating Identidad:\n"
                    for error in error.errors():
                        error_string += f"\tError validating: {error['loc'][0]}\n"
                    error_string += "Aborting"
                    return error_string

                direccion = {
                    "Address type": None,
                    "Address": None,
                    "Postal code": None,
                    "Community": None,
                    "City": None
                }

                for key in direccion:
                    if key == "Address type":
                        print(
                            f"Available types: {', '.join([t.value for t in ViaType])}")
                    if key == "Postal code":
                        print("Must be 5 digits")

                    aux = input(f"{key.capitalize()}: ")

                    if len(aux) < 2:
                        return f"Invalid value for {key.capitalize()}"
                    if key == "Postal code" and len(aux) != 5:
                        return f"Invalid value for {key.capitalize()}. Must be 5 digits"
                    if key == "Address type":
                        try:
                            aux = ViaType(aux)
                        except ValueError:
                            return f"Invalid adress type: {aux}"
                    direccion[key] = aux

                try:
                    direccion = Direcion(**direccion)
                except ValidationError as error:
                    log.error(error)
                    error_string = "Encountered the following errors when validating Identidad:\n"
                    for error in error.errors():
                        error_string += f"\tError validating: {error['loc'][0].capitalize()}\n"
                    error_string += "Aborting"
                    return error_string

                citizen = Citizen(identidad=identidad, direccion=direccion)

                print("Readed citizen info:")
                print(self.__format_citizen(citizen))
                aux = input("Is this info correct? (y/n): ")
                if aux.lower() == "y":
                    return service.signup_citizen(citizen)
                else:
                    return "Signup aborted"

    def __update_citizen_by_key(self, citizen:Citizen, updatable_key, new):
        match updatable_key:
            case "Name":
                citizen.identidad.nombre = new
            case "Surname":
                citizen.identidad.apellidos = new
            case "NI":
                citizen.identidad.ni = new
            case "Address type":
                citizen.direccion.type = new
            case "Address":
                citizen.direccion.direccion = new
            case "Postal code":
                citizen.direccion.codigo_postal = new
            case "Community":
                citizen.direccion.comunidad = new
            case "City":
                citizen.direccion.ciudad = new

    def __get_old_by_key(self, citizen, updatable_key):
        match updatable_key:
            case "Name":
                old = citizen.identidad.nombre
            case "Surname":
                old = citizen.identidad.apellidos
            case "NI":
                old = citizen.identidad.ni
            case "Address type":
                old = citizen.direccion.type.value
                print(
                            f"Available types: {', '.join([t.value for t in ViaType])}")
            case "Address":
                old = citizen.direccion.direccion
            case "Postal code":
                old = citizen.direccion.codigo_postal
                print("Must be 5 digits")
            case "Community":
                old = citizen.direccion.comunidad
            case "City":
                old = citizen.direccion.ciudad
        return old
