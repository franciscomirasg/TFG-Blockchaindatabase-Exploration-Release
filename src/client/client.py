from datetime import datetime
import json
from typing import Callable, Dict, List, Literal, Union
from uuid import uuid4

from requests.exceptions import HTTPError

import interfaces.data_interfaces as data_interfaces
from interfaces.request import EventOut
import interfaces.trash as trash
import utils.subject_factory as factory
from client.shell import Shell
from command.command import Command
from config import global_settings
from interfaces.citizen import Citizen
from interfaces.event import ApprovalType, Event, EventRequest
from interfaces.subject import Subject
from interfaces.trash import (PointTransaction, PointTransactionEvent,
                              calculate_points)
from utils.logs import log
from utils.persistence import Persistence
from utils.taple_connector import RestConnector

from static.shop import ShopItem
from requests.exceptions import ConnectionError

import subprocess


class Client:
    """
    Client for the recycle zone
    """

    def __init__(self, name: str, commands: List[Command]) -> None:
        self.persistence = Persistence(f"./data/{name}.db")
        self.shell = Shell(
            commands,
            self
        )
        self.rest_connector = None

        # Search for init data
        init_data = self.get_connection_data()
        if init_data and "host" in init_data and "port" in init_data and "api_key" in init_data:
            log.info(f"Init connector with data: {init_data}")
            self.init_connector(**init_data)

        self.shell.start()

    def init_connector(self, host: str, port: int, api_key: str):
        """
        Init connector
        """
        self.rest_connector = RestConnector(host, port, api_key)

    def get_connection_data(self):
        """
        Get connection data
        """
        return self.persistence.get(global_settings.connection_key)

    def set_connection_data(self, data: dict):
        """
        Set connection data
        """
        self.persistence.put(global_settings.connection_key, data)
        self.init_connector(**data)

    def get_self(self) -> Dict[Literal["id", "subject_id"], str]:
        """
        Get self data, necesary for self information. 
        For citizen map cuid with subject_id.
        """
        result = self.persistence.get("self")
        if result is None:
            return {
                "id": str(uuid4()),
                "subject_id": None
            }
        self.persistence.put("self", result)
        return self.persistence.get("self")

    def search_wallet(self, cuid: str) -> Union[PointTransaction, str] | None:
        """
        Search for the citizen wallet
        """
        results = self.__list_all_subjects(
            lambda subject: subject.schema_id == global_settings.point_transaction_schema)
        found = None
        for subject in results:
            subject_id = subject.subject_id
            subject: PointTransaction = factory.schema_to_object(
                global_settings.point_transaction_schema, subject)
            if subject.cuid == cuid:
                found = (subject, subject_id)
                break
        return found

    def get_citizen_location(self, cuid:str) -> None | data_interfaces.CitizenHost:
        """
        Get citizen location
        """
        citizen = self.persistence.get(cuid)
        if citizen is None:
            return None
        return citizen
    
    def set_citizen_location(self, cuid:str, citizen_host: data_interfaces.CitizenHost) -> None:
        """
        Set citizen location
        """
        self.persistence.put(cuid, citizen_host)

    def reward_points(self, cuid: str, recycle_info: trash.RecycleOperation) -> str:
        """
        Reward points to citizen.
        If error log it
        """

        wallet = self.search_wallet(cuid)
        if wallet is None:
            log.warning(f"Wallet not found for citizen {cuid}")
            return f"Wallet not found for citizen {cuid}"

        wallet, subject_id = wallet

        points = calculate_points(recycle_info.type, recycle_info.peso)

        wallet.value = points
        wallet.balance += points
        wallet.motivo = "Recycle Program Rewards"

        request = factory.make_wallet_update(wallet, subject_id)
        try:
            request = self.__make_external_request(request)
        except Exception as error: # pylint: disable=broad-exception-caught
            if not isinstance(error, IOError):
                log.error(error)
            return "Error adding with signature. Aborting"
        connection = self.get_citizen_location(cuid)
        if connection is None:
            return "Citizen location not found"


        try:
            self.rest_connector.create_external_event_request(
                connection.host, connection.port, request)
            return f"Rewards added to citizen {cuid}"
        except Exception as error: # pylint: disable=broad-exception-caught
            if isinstance(error, ConnectionError):
                self.persistence.delete(cuid)
                return "Citizen location invalid. Data removed.\nRewards not added."
            log.error(error)

    def __make_external_request(self, request: EventOut) -> EventOut:
        payload = request.get_signable_payload()
        apy_key = self.get_connection_data()["api_key"]
        
        cmd = [
            global_settings.sign_tool,
            apy_key,
            json.dumps(payload)
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True, check=False
        )

        if result.returncode != 0:
            log.error(result.stderr)
            raise IOError("Error signing request")
        
        return EventOut(**json.loads(result.stdout))

    def make_recycle_opperation(self, recycle_data: trash.RecycleOperation) -> str: 
        """
        Create or update a recycle operation.
        Append points to the citizen
        """
        if self.rest_connector is None:
            return "Connector not initialized"

        container_info = self.get_self()
        recycle_data.container = container_info["id"]
        try:
            if container_info["subject_id"] is None:
                request = factory.make_create_recycle_op(recycle_data)
                result = self.rest_connector.create_event_request(request)
                container_info["subject_id"] = result.subject_id
                self.persistence.put("self", container_info)
            else:
                request = factory.make_update_recycle_op(
                    recycle_data, container_info["subject_id"])
                result = self.rest_connector.create_event_request(request)
            return "Recycle Trazed added"
        except HTTPError as error:
            log.error(error)
            return "Error creating recycle operation"

    def list_containers(self) -> data_interfaces.SubjectMapList:
        """
        List all recycle zones int the system.
        """
        result = self.persistence.get(global_settings.recycle_zones_key)
        if result is None:
            return data_interfaces.SubjectMapList(
                last_update=None,
                map_list=[]
            )
        return result

    def __list_all_subjects(self, filter_: Callable[[Subject], bool] = None) -> List[Subject]:
        batch = 10
        limit = 0
        searching = True
        results = []
        while searching:
            try:
                batch_result = self.rest_connector.get_all_subjects_data(
                    limit, batch)
                if len(batch_result) < batch:
                    searching = False
                if filter_:
                    for subject in batch_result:
                        if filter_(subject):
                            results.append(subject)
                else:
                    results += batch_result
                limit += batch
            except HTTPError as error:
                if error.response.status_code == 404:
                    searching = False
                else:
                    log.error(error)
                    return "Error searching subjects"
        return results

    def search_containers(self) -> data_interfaces.SubjectMapList:
        """
        Search for containers in the system
        """
        if self.rest_connector is None:
            return "Connector not initialized"

        results = self.__list_all_subjects(
            lambda subject: subject.schema_id == global_settings.recycle_schema)
        data = data_interfaces.SubjectMapList(
            last_update=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            map_list=[
                {
                    "id": subject.properties["container"],
                    "subject_id": subject.subject_id
                } for subject in results
            ]
        )
        self.persistence.put(
            global_settings.recycle_zones_key,
            data
        )
        return data

    def __list_all_events_from_subject(self, subject_id: str) -> List[Event]:
        batch = 10
        limit = 0
        searching = True
        results = []
        while searching:
            try:
                batch_result = self.rest_connector.get_subject_events(
                    subject_id, limit, batch)
                if len(batch_result) < batch:
                    searching = False
                results += batch_result
                limit += batch
            except HTTPError as error:
                if error.response.status_code == 404:
                    searching = False
                else:
                    log.error(error)
                    return "Error searching subjects"
        return results

    def list_recycle_by_container(self, container_id: str) -> List[trash.RecycleOperationEvent]:
        """
        List recycle operations by container
        """

        if self.rest_connector is None:
            return "Connector not initialized"

        containers: data_interfaces.SubjectMapList = self.persistence.get(
            global_settings.recycle_zones_key)
        found = False
        for container in containers.map_list:
            if container.id == container_id:
                found = True
                break
        if not found:
            return "Container not found"
        results = self.__list_all_events_from_subject(container.subject_id)
        return [
            trash.RecycleOperationEvent(
                data=factory.properties_to_object(
                    global_settings.recycle_schema,
                    event.event_content.event_request.request.payload.json_
                ),
                timestamp=event.event_content.event_request.timestamp
            ) for event in results
        ]

    def list_recycle_all_containers(self) -> List[trash.RecycleOperationEvent]:
        """
        List recycle operations by container
        """

        if self.rest_connector is None:
            return "Connector not initialized"

        containers: data_interfaces.SubjectMapList = self.persistence.get(
            global_settings.recycle_zones_key)
        results: List[Event] = []
        for container in containers.map_list:
            results += self.__list_all_events_from_subject(
                container.subject_id)
        results.sort(
            key=lambda event: event.event_content.event_request.timestamp)
        return [
            trash.RecycleOperationEvent(
                data=factory.properties_to_object(
                    global_settings.recycle_schema,
                    event.event_content.event_request.request.payload.json_
                ),
                timestamp=event.event_content.event_request.timestamp
            ) for event in results
        ]

    def get_citizen_info(self, cuid: str | None = None) -> Citizen | None:
        """
        Get citizen information.
        If cuid is None, return the information of self
        """
        if self.rest_connector is None:
            return "Connector not initialized"

        if cuid is None:
            me = self.get_self()
            if me["subject_id"] is None:
                return None
            try:
                result = self.rest_connector.get_subject_by_id(
                    me["subject_id"])
            except HTTPError as error:
                if error.response.status_code == 404:
                    me["subject_id"] = None
                    self.persistence.put(global_settings.self_key, me)
                    return None
                else:
                    log.error(error)
                    return None
            return factory.schema_to_object(global_settings.citizen_schema, result)
        else:
            citizens: data_interfaces.SubjectMapList = self.persistence.get(
                global_settings.citizens_key)
            for citizen in citizens.map_list:
                if citizen.id == cuid:
                    try:
                        result = self.rest_connector.get_subject_by_id(
                            citizen.subject_id)
                    except HTTPError as error:
                        if error.response.status_code == 404:
                            return None
                        else:
                            log.error(error)
                            return None
                    return factory.schema_to_object(global_settings.citizen_schema, result)
            return None

    def signup_citizen(self, citezen: Citizen) -> str:
        """
        Signup a new citizen
        """

        if self.rest_connector is None:
            return "Connector not initialized"

        try:
            request = factory.make_create_citizen(citezen)
            result = self.rest_connector.create_event_request(request)
            me = {
                "id": citezen.cuid,
                "subject_id": result.subject_id
            }
            self.persistence.put(global_settings.self_key, me)
            return "Citizen created. If you want use points commands and create a reward wallet."
        except HTTPError as error:
            log.error(error)
            return "Error creating citizen. Try later"

    def update_citizen(self, citizen: Citizen) -> str:
        """
        Update citizen information
        """

        if self.rest_connector is None:
            return "Connector not initialized"

        me = self.get_self()
        if me["subject_id"] is None:
            return "Citizen not found"

        try:
            request = factory.make_update_citizen(citizen, me["subject_id"])
            self.rest_connector.create_event_request(request)
            return "Citizen update posted. Wait for approval."
        except HTTPError as error:
            log.error(error)
            return "Error updating citizen. Try later"

    def get_wallet(self) -> PointTransaction | None:
        """
        Get wallet information, If wallet is not found, return None
        """

        if self.rest_connector is None:
            return "Connector not initialized"

        wallet = self.persistence.get(global_settings.wallet_key)
        if wallet is None:
            return None

        try:
            result = self.rest_connector.get_subject_by_id(
                wallet["subject_id"])
            return factory.schema_to_object(global_settings.point_transaction_schema, result)
        except HTTPError as error:
            if error.response.status_code != 404:
                log.error(error)
            return None

    def init_wallet(self) -> PointTransaction | None:
        """
        Initialize wallet
        If wallet is already initialized, return wallet
        If citizen is not found, return None.
        Errors are returned as string
        """

        if self.rest_connector is None:
            return "Connector not initialized"

        me = self.get_self()
        if me["subject_id"] is None:
            return None

        wallet = self.get_wallet()

        if wallet is not None:
            return wallet

        wallet = PointTransaction(
            cuid=me["id"],
            balance=10,
            value=10,
            motivo="Wallet Created. Welcome to the system"
        )

        try:
            request = factory.make_wallet_create(wallet)
            result = self.rest_connector.create_event_request(request)
            self.persistence.put(global_settings.wallet_key, {
                "cuid": me["id"],
                "subject_id": result.subject_id
            })
            return wallet
        except HTTPError as error:
            log.error(error)
            return "Error creating wallet. Try later"

    def get_wallet_history(self) -> List[PointTransactionEvent]:
        """
        Get wallet history
        """
        if self.rest_connector is None:
            return "Connector not initialized"

        wallet = self.persistence.get(global_settings.wallet_key)
        if wallet is None:
            return "Not wallet found"

        try:
            results = self.__list_all_events_from_subject(wallet["subject_id"])
            return [
                PointTransactionEvent(
                    data=factory.properties_to_object(
                        global_settings.point_transaction_schema,
                        event.event_content.event_request.request.payload.json_
                    ),
                    timestamp=event.event_content.event_request.timestamp
                ) for event in results
            ]
        except HTTPError as error:
            log.error(error)
            return "Error getting wallet history"

    def buy_item(self, item: ShopItem):
        """
        Buy an item
        """
        if self.rest_connector is None:
            return "Connector not initialized"

        wallet = self.get_wallet()
        if wallet is None:
            return "Wallet not found, execute points first"

        if wallet.balance < item.price:
            return "Not enough points for redeem this item"

        subject_id = self.persistence.get(
            global_settings.wallet_key)["subject_id"]

        wallet.balance -= item.price
        wallet.value = -item.price
        wallet.motivo = f"Item {item.name} bought. Item ID: {item.article_id}"

        try:
            request = factory.make_wallet_update(wallet, subject_id)
            self.rest_connector.create_event_request(request)
            return "Item Bought. Wait until city hall approve the transaction and ship the item."
        except HTTPError as error:
            log.error(error)
            return "Error buying item. Try later"

    def search_citizen(self) -> data_interfaces.SubjectMapList:
        """
        Search for citizens in the system
        """
        if self.rest_connector is None:
            return "Connector not initialized"

        results = self.__list_all_subjects(
            lambda subject: subject.schema_id == global_settings.citizen_schema)
        data = data_interfaces.SubjectMapList(
            last_update=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            map_list=[
                {
                    "id": subject.properties["cuid"],
                    "subject_id": subject.subject_id
                } for subject in results
            ]
        )
        self.persistence.put(
            global_settings.citizens_key,
            data
        )
        return data

    def list_citizen(self) -> data_interfaces.SubjectMapList:
        """
        List all citizens int the system.
        """
        result = self.persistence.get(global_settings.citizens_key)
        if result is None:
            return data_interfaces.SubjectMapList(
                last_update=None,
                map_list=[]
            )
        return result

    def get_citizen_by_id(self, cuid: str) -> Citizen:
        """
        Get recycle operations by container
        """

        if self.rest_connector is None:
            return "Connector not initialized"

        containers: data_interfaces.SubjectMapList = self.persistence.get(
            global_settings.citizens_key)
        found = False
        for citizen_info in containers.map_list:
            if citizen_info.id == cuid:
                found = True
                break
        if not found:
            return "Citizen not found. Try search for citizens first"

        try:
            result = self.rest_connector.get_subject_by_id(
                citizen_info.subject_id)
        except HTTPError as error:
            if error.response.status_code != 404:
                return "Citizen not found. Try search for citizens first"
            log.error(error)
            return "Error getting citizen. Try later"

        return factory.schema_to_object(global_settings.citizen_schema, result)

    def list_all_citizens(self) -> List[Citizen]:
        """
        List all citizens
        """

        if self.rest_connector is None:
            return "Connector not initialized"

        citizens = self.__list_all_subjects(
            lambda subject: subject.schema_id == global_settings.citizen_schema)
        
        data = data_interfaces.SubjectMapList(
            last_update=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            map_list=[
                {
                    "id": subject.properties["cuid"],
                    "subject_id": subject.subject_id
                } for subject in citizens
            ]
        )
        self.persistence.put(global_settings.citizens_key, data)

        return [
            factory.schema_to_object(global_settings.citizen_schema, citizen) for citizen in citizens
        ]

    def get_approvals(self) -> List[EventRequest]:
        """
        Retrieve all approvals
        """
        if self.rest_connector is None:
            return "Connector not initialized"

        approvals = []

        try:
            approvals = self.rest_connector.get_pending_approvals()
        except HTTPError as error:
            log.error(error)
            return "Error getting approvals. Try later"
        
        return approvals
    
    def get_subject(self, subject_id:str) -> Subject|None:
        """
        Get subject by id
        """
        if self.rest_connector is None:
            return "Connector not initialized"
        try:
            return self.rest_connector.get_subject_by_id(subject_id)
        except HTTPError as error:
            if error.response.status_code != 404:
                return None
            log.error(error)
            return None
        
    def resolve_approval(self, approval:EventRequest, value = ApprovalType) -> str:
        """
        Resolve an approval
        """
        if self.rest_connector is None:
            return "Connector not initialized"
        
        request = factory.make_approval(value)
        try:
            self.rest_connector.put_approval_for_request(approval.request_id, request)
            return "Approval resolved"
        except HTTPError as error:
            if error.response.status_code != 404:
                return "Approval not found"
            log.error(error)
            return "Error resolving approval. Try later"
    