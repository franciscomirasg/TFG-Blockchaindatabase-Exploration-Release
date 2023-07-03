from interfaces.approval import ApprovalResponse
import interfaces.trash as trash
import interfaces.citizen as citizen
from config import global_settings
from interfaces.request import EventOut
from interfaces.event import ApprovalType, Request, Create, Payload, State
from interfaces.subject import Subject
import interfaces.data_interfaces as data_interfaces

SCHEMA_TO_CLS = {
    global_settings.recycle_schema: trash.RecycleOperation,
    global_settings.point_transaction_schema: trash.PointTransaction,
    global_settings.citizen_schema: citizen.Citizen,
    trash.RecycleOperationEvent.__name__: trash.RecycleOperationEvent,
}

MODELS_TO_CLS = {
    data_interfaces.SubjectMapList.__name__: data_interfaces.SubjectMapList,
    data_interfaces.CitizenHost.__name__: data_interfaces.CitizenHost,
}


def schema_to_object(schema_id: str, subject: Subject) -> trash.PointTransaction | trash.RecycleOperation | citizen.Citizen:
    """
    Convert a schema to a object
    """
    cls = SCHEMA_TO_CLS[schema_id]
    return cls(**subject.properties)

def properties_to_object(schema_id: str, event: dict) -> trash.PointTransaction | trash.RecycleOperation | citizen.Citizen:
    """
    Convert a event to a model
    """
    cls = SCHEMA_TO_CLS[schema_id]
    return cls(**event)

def dict_to_model(model:str, data:dict) -> data_interfaces.SubjectMapList:
    """
    Convert a dict to a model
    """
    cls = MODELS_TO_CLS[model]
    return cls(**data)

def make_create_recycle_op(recycle_data: trash.RecycleOperation) -> EventOut:
    """
    Create a recycle operation Request
    """
    return EventOut(
        request=Request(
            create=Create(
                governance_id=global_settings.governance_id,
                namespace="",
                schema_id="RecycleOperation",
                payload=Payload(
                    Json=recycle_data.dict()
                )
            ),
        )
    )

def make_create_citizen(citizen_data: citizen.Citizen) -> EventOut:
    """
    Create a citizen Request
    """
    return EventOut(
        request=Request(
            create=Create(
                governance_id=global_settings.governance_id,
                namespace="",
                schema_id=global_settings.citizen_schema,
                payload=Payload(
                    Json=citizen_data.dict()
                )
            ),
        )
    )

def make_wallet_create(wallet: trash.PointTransaction) -> EventOut:
    """
    Create a wallet Request
    """
    return EventOut(
        request=Request(
            create=Create(
                governance_id=global_settings.governance_id,
                namespace="",
                schema_id=global_settings.point_transaction_schema,
                payload=Payload(
                    Json=wallet.dict()
                )
            ),
        )
    )

def make_wallet_update(wallet: trash.PointTransaction, subject_id: str) -> EventOut:
    """
    Update a wallet Request
    """
    return EventOut(
        request=Request(
            state=State(
                subject_id=subject_id,
                payload=Payload(
                    Json=wallet.dict()
                )
            )
        )
    )

def make_update_citizen(citizen_data: citizen.Citizen, subject_id: str) -> EventOut:
    """
    Update a citizen Request
    """
    return EventOut(
        request=Request(
            state=State(
                subject_id=subject_id,
                payload=Payload(
                    Json=citizen_data.dict()
                )
            )
        )
    )

def make_update_recycle_op(recycle_data: trash.RecycleOperation, subject_id: str) -> EventOut:
    """
    Update a recycle operation Request
    """
    return EventOut(
        request=Request(
            state=State(
                subject_id=subject_id,
                payload=Payload(
                    Json=recycle_data.dict()
                )
            )
        )
    )

def make_approval(value: ApprovalType) -> ApprovalResponse:
    """
    Create a approval response
    """
    return ApprovalResponse(
        approvalType=value
    )
