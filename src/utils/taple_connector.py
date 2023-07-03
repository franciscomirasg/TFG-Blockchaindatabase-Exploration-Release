from typing import List
import json
import requests

from interfaces.event import Event, Request, EventRequest
from interfaces.subject import Subject
from interfaces.request import EventOut, EventIn
from interfaces.approval import ApprovalResponse

from rich import print

class RestConnector:
    """
    Rest connector for TAPLE node
    """

    def __init__(self, host:str, port:int, api_key:str):
        self.__base_url = f"{host}:{port}"
        self.__api_key = api_key


    def get(self, endpoint: str, params=None):
        """
        Generic GET request
        """
        url = f"{self.__base_url}{endpoint}"
        headers = {"x-api-key": self.__api_key, 'Accept': 'application/json'}
        response = requests.get(url, headers=headers, params=params, timeout=60)
        response.raise_for_status()
        return response.json()

    def external_post(self, host:str, port:int, endpoint: str, payload: str):
        """
        Generic POST used for external requests
        """
        url = f"{host}:{port}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers,
                                 data=payload, timeout=60)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, payload: str):
        """
        Generic POST request
        """
        url = f"{self.__base_url}{endpoint}"
        headers = {"x-api-key": self.__api_key,
                   'Accept': 'application/json', 'Content-Type': 'application/json'}
        print(payload)
        response = requests.post(url, headers=headers,
                                 data=payload, timeout=60)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, payload: dict):
        """
        Generic PUT request
        """
        url = f"{self.__base_url}{endpoint}"
        headers = {"x-api-key": self.__api_key,
                   'Accept': 'application/json', 'Content-Type': 'application/json'}
        response = requests.put(url, headers=headers, data=payload, timeout=60)
        response.raise_for_status()
        return response.json()

    def get_all_subjects_data(self, from_value: int, quantity: int) -> List[Subject]:
        """
        Get all subjects data
        """
        response = self.get(
            "/api/subjects", params={"from": from_value, "quantity": quantity})
        return [Subject(**subject) for subject in response]

    def get_subject_by_id(self, subject_id: str) -> Subject:
        """
        Get subject by id
        """
        response = self.get(f"/api/subjects/{subject_id}")
        return Subject(**response)

    def get_subject_events(self, subject_id: str, from_value: int, quantity: int) -> List[Event]:
        """
        Get subject events
        """
        response = self.get(
            f"/api/subjects/{subject_id}/events", params={"from": from_value, "quantity": quantity})
        return [Event(**event) for event in response]

    def get_subject_event_by_sn(self, subject_id: str, sn: int) -> Event:
        """
        Get subject event by sn
        """
        response = self.get(f"/api/subjects/{subject_id}/events/{sn}")
        return Event(**response)

    def get_event_properties(self, subject_id, sn) -> Request:
        """
        Get event properties
        """
        response = self.get(
            f"/api/subjects/{subject_id}/events/{sn}/properties")
        return Request(**response)

    def create_event_request(self, payload: EventOut) -> EventIn:
        """
        Create event request
        """
        response = self.post("/api/requests", json.dumps(payload.to_request()))
        return EventIn(**response)

    def create_external_event_request(self, host:str, port:int, payload: EventOut) -> EventIn:
        """
        Create external event request
        """
        response = self.external_post(host, port, "/api/requests", json.dumps(payload.to_request()))
        return EventIn(**response)

    def get_pending_approvals(self) -> List[EventRequest]:
        """
        Get all the pending requests for Approval
        """
        response = self.get("/api/approvals")
        print(response)
        return [EventRequest(**approval) for approval in response]

    def get_pending_approval_by_id(self, approval_id: str) -> EventRequest:
        """
        Get pending approval by id
        """
        response = self.get(f"/api/approvals/{approval_id}")
        return EventRequest(**response)

    def put_approval_for_request(self, approval_id: str, payload: ApprovalResponse) -> None:
        """
        Set your Aprroval for a request
        """
        self.put(f"/api/approvals/{approval_id}", json.dumps(payload.dict(by_alias=True)))
