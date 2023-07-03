from datetime import datetime

import pytest

from interfaces.approval import ApprovalResponse
from interfaces.event import (Approval, ApprovalType, ContentApproval,
                              ContentSignature, Create, Event, EventContent,
                              EventRequest, Metadata, Payload, Request,
                              Signature, State)
from interfaces.request import EventIn, EventOut
from interfaces.subject import Subject

now = datetime(2023, 6, 25)


@pytest.fixture
def get_now():  # pylint: disable=missing-function-docstring
    return now


subject_schema_1: dict = {
    "governance_id": "string",
    "namespace": "string",
    "owner": "string",
    "properties": {"foo": "bar"},
    "public_key": "string",
    "schema_id": "string",
    "sn": 0,
    "subject_id": "string"
}

subject_schema_2: dict = {
    "governance_id": "J7BgD3dqZ8vO4WEH7-rpWIH-IhMqaSDnuJ3Jb8K6KvL0",
    "namespace": "namespace1",
    "owner": "EFXv0jBIr6BtoqFMR7G_JBSuozRc2jZnu5VGUH2gy6-w",
    "properties": {"localizacion": "España", "temperatura": 10},
    "public_key": "ELZ_b-kZzdPykcYuRNC2ZZe_2lCTCUoo60GXfR4cuXMw",
    "schema_id": "Prueba",
    "sn": 0,
    "subject_id": "JKZgYhPjQdWNWWwkac0wSwqLKoOJsT0QimJmj6zjimWc"
}

subject_1: Subject = Subject(
    governance_id="string",
    namespace="string",
    owner="string",
    properties={"foo": "bar"},
    public_key="string",
    schema_id="string",
    sn=0,
    subject_id="string"
)

subject_2: Subject = Subject(
    governance_id="J7BgD3dqZ8vO4WEH7-rpWIH-IhMqaSDnuJ3Jb8K6KvL0",
    namespace="namespace1",
    owner="EFXv0jBIr6BtoqFMR7G_JBSuozRc2jZnu5VGUH2gy6-w",
    properties={"localizacion": "España", "temperatura": 10},
    public_key="ELZ_b-kZzdPykcYuRNC2ZZe_2lCTCUoo60GXfR4cuXMw",
    schema_id="Prueba",
    sn=0,
    subject_id="JKZgYhPjQdWNWWwkac0wSwqLKoOJsT0QimJmj6zjimWc"
)


@pytest.fixture
def get_subject_schema_1():  # pylint: disable=missing-function-docstring
    return subject_schema_1


@pytest.fixture
def get_subject_schema_2():  # pylint: disable=missing-function-docstring
    return subject_schema_2


@pytest.fixture
def get_subject_1():  # pylint: disable=missing-function-docstring
    return subject_1


@pytest.fixture
def get_subject_2():  # pylint: disable=missing-function-docstring
    return subject_2


@pytest.fixture
def get_all_subjects():  # pylint: disable=missing-function-docstring
    return [subject_1, subject_2]


@pytest.fixture
def get_all_subjects_schema():  # pylint: disable=missing-function-docstring
    return [subject_schema_1, subject_schema_2]


request_state_schema = {
    "State": {
        "payload": {
            "Json": {"localizacion": "Argentina",
                     "temperatura": -3}
        },
        "subject_id": "JKZgYhPjQdWNWWwkac0wSwqLKoOJsT0QimJmj6zjimWc"
    }
}

request_create_schema = {
    "Create": {
        "governance_id": "string",
        "namespace": "string",
        "payload": {
            "Json": {"foo": "bar"}
        },
        "schema_id": "string"
    }
}

request_create = Request(
    create=Create(
        governance_id="string",
        namespace="string",
        payload=Payload(
            json_={"foo": "bar"}
        ),
        schema_id="string"
    )
)

request_state = Request(
    state=State(
        payload=Payload(
            json_={"localizacion": "Argentina",
                   "temperatura": -3}
        ),
        subject_id="JKZgYhPjQdWNWWwkac0wSwqLKoOJsT0QimJmj6zjimWc"
    )
)


@pytest.fixture
def get_request_state_schema():  # pylint: disable=missing-function-docstring
    return request_state_schema


@pytest.fixture
def get_request_create_schema():  # pylint: disable=missing-function-docstring
    return request_create_schema


@pytest.fixture
def get_request_create():  # pylint: disable=missing-function-docstring
    return request_create


@pytest.fixture
def get_request_state():  # pylint: disable=missing-function-docstring
    return request_state


event_1_schema = {
    "event_content": {
        "approved": True,
        "event_request": {
            "approvals": [],
            "request": {
                "State": {
                    "payload": {
                        "Json": {"localizacion": "Argentina", "temperatura": -3}
                    },
                    "subject_id": "JKZgYhPjQdWNWWwkac0wSwqLKoOJsT0QimJmj6zjimWc"
                }
            },
            "signature": {
                "content": {
                    "event_content_hash": "JBmfwxOtP2gXFzyTQX0NzVw8ByiHjxcyBgaBamYoOhcA",
                    "signer": "EFXv0jBIr6BtoqFMR7G_JBSuozRc2jZnu5VGUH2gy6-w",
                    "timestamp": 1671706794
                },
                "signature": "SEuYCV5T0G4Vpps859QQMzimXw8NcYailkXwh2oKtsVX82iJQzbspKR7nLllcHiKfuWRkzCWbFpQzxPBWdsuZgBA"
            },
            "timestamp": 1671706794
        },
        "metadata": {
            "governance_id": "J7BgD3dqZ8vO4WEH7-rpWIH-IhMqaSDnuJ3Jb8K6KvL0",
            "governance_version": 0,
            "namespace": "namespace1",
            "owner": "EFXv0jBIr6BtoqFMR7G_JBSuozRc2jZnu5VGUH2gy6-w",
            "schema_id": "Prueba"
        },
        "previous_hash": "JnMRtYtb2DD2cueHe4oAVMJUoqtkexwZa_n6WWFmH8eA",
        "sn": 1,
        "state_hash": "JMqLbPz7VY1pjuj9-n0qT0UuOGH_TpQVRaVEOHSaE_5Y",
        "subject_id": "JKZgYhPjQdWNWWwkac0wSwqLKoOJsT0QimJmj6zjimWc"
    },
    "signature": {
        "content": {
            "event_content_hash": "JYkgipgpilkVFVV_hJ0Dxvr2eHmXU6niKTmKSjMVYEZY",
            "signer": "ELZ_b-kZzdPykcYuRNC2ZZe_2lCTCUoo60GXfR4cuXMw",
            "timestamp": 1671706794
        },
        "signature": "SEDcHW5nM7HPsQJyHQkAVaV5NkTuwT2fJL_T9r0HmqbgT3Wt7AMTFpjJNunlCSa-dEosItNu5P9k05vAE9064TBg"
    }
}

event_2_schema = {
    "event_content": {
        "approved": True,
        "event_request": {
            "approvals": [
                {
                    "content": {
                        "approval_type": "Accept",
                        "event_request_hash": "string",
                        "expected_sn": 0,
                        "signer": "string",
                        "timestamp": 0
                    },
                    "signature": "string"
                }
            ],
            "request": {
                "Create": {
                    "governance_id": "string",
                    "namespace": "string",
                    "payload": {
                        "Json": {"foo": "bar"}
                    },
                    "schema_id": "string"
                }
            },
            "signature": {
                "content": {
                    "event_content_hash": "string",
                    "signer": "string",
                    "timestamp": 0
                },
                "signature": "string"
            },
            "timestamp": 0
        },
        "metadata": {
            "governance_id": "string",
            "governance_version": 0,
            "namespace": "string",
            "owner": "string",
            "schema_id": "string"
        },
        "previous_hash": "string",
        "sn": 0,
        "state_hash": "string",
        "subject_id": "string"
    },
    "signature": {
        "content": {
            "event_content_hash": "string",
            "signer": "string",
            "timestamp": 0
        },
        "signature": "string"
    }
}

event_1 = Event(
    event_content=EventContent(
        approved=True,
        event_request=EventRequest(
            approvals=[],
            request=request_state,
            signature=Signature(
                content=ContentSignature(
                    event_content_hash="JBmfwxOtP2gXFzyTQX0NzVw8ByiHjxcyBgaBamYoOhcA",
                    signer="EFXv0jBIr6BtoqFMR7G_JBSuozRc2jZnu5VGUH2gy6-w",
                    timestamp=1671706794
                ),
                signature="SEuYCV5T0G4Vpps859QQMzimXw8NcYailkXwh2oKtsVX82iJQzbspKR7nLllcHiKfuWRkzCWbFpQzxPBWdsuZgBA"
            ),
            timestamp=1671706794
        ),
        metadata=Metadata(
            governance_id="J7BgD3dqZ8vO4WEH7-rpWIH-IhMqaSDnuJ3Jb8K6KvL0",
            governance_version=0,
            namespace="namespace1",
            owner="EFXv0jBIr6BtoqFMR7G_JBSuozRc2jZnu5VGUH2gy6-w",
            schema_id="Prueba"
        ),
        previous_hash="JnMRtYtb2DD2cueHe4oAVMJUoqtkexwZa_n6WWFmH8eA",
        sn=1,
        state_hash="JMqLbPz7VY1pjuj9-n0qT0UuOGH_TpQVRaVEOHSaE_5Y",
        subject_id="JKZgYhPjQdWNWWwkac0wSwqLKoOJsT0QimJmj6zjimWc"
    ),
    signature=Signature(
        content=ContentSignature(
            event_content_hash="JYkgipgpilkVFVV_hJ0Dxvr2eHmXU6niKTmKSjMVYEZY",
            signer="ELZ_b-kZzdPykcYuRNC2ZZe_2lCTCUoo60GXfR4cuXMw",
            timestamp=1671706794
        ),
        signature="SEDcHW5nM7HPsQJyHQkAVaV5NkTuwT2fJL_T9r0HmqbgT3Wt7AMTFpjJNunlCSa-dEosItNu5P9k05vAE9064TBg"
    )
)

event_2 = Event(
    event_content=EventContent(
        approved=True,
        event_request=EventRequest(
            approvals=[
                Approval(
                    content=ContentApproval(
                        approval_type="Accept",
                        event_request_hash="string",
                        expected_sn=0,
                        signer="string",
                        timestamp=0
                    ),
                    signature="string"
                )
            ],
            request=request_create,
            signature=Signature(
                content=ContentSignature(
                    event_content_hash="string",
                    signer="string",
                    timestamp=0
                ),
                signature="string"
            ),
            timestamp=0
        ),
        metadata=Metadata(
            governance_id="string",
            governance_version=0,
            namespace="string",
            owner="string",
            schema_id="string"
        ),
        previous_hash="string",
        sn=0,
        state_hash="string",
        subject_id="string"
    ),
    signature=Signature(
        content=ContentSignature(
            event_content_hash="string",
            signer="string",
            timestamp=0
        ),
        signature="string"
    )
)


@pytest.fixture
def get_event_1():
    return event_1


@pytest.fixture
def get_event_2():
    return event_2


@pytest.fixture
def get_event_1_schema():
    return event_1_schema


@pytest.fixture
def get_event_2_schema():
    return event_2_schema


@pytest.fixture
def get_events_schema():
    return [event_1_schema, event_2_schema]


@pytest.fixture
def get_events():
    return [event_1, event_2]


create_event_1_out_schema = {
    "request": {
        "Create": {
            "governance_id": "string",
            "namespace": "string",
            "payload": {
                "Json": {
                    "foo": "bar"
                }
            },
            "schema_id": "string"
        }
    },
    "signature": {
        "content": {
            "event_content_hash": "string",
            "signer": "string",
            "timestamp": 0
        },
        "signature": "string"
    },
    "timestamp": 1
}

create_event_2_out_schema = {
    "request": {
        "State": {
            "subject_id": "string",
            "payload": {
                "Json": {
                    "foo": "bar"
                }
            },
        }
    },
    "signature": {
        "content": {
            "event_content_hash": "string",
            "signer": "string",
            "timestamp": 0
        },
        "signature": "string"
    },
    "timestamp": 2
}

create_event_1_out = EventOut(
    request=Request(
        create=Create(
            governance_id="string",
            namespace="string",
            payload=Payload(
                json_={
                    "foo": "bar"
                }
            ),
            schema_id="string"

        )
    ),
    signature=Signature(
        content=ContentSignature(
            event_content_hash="string",
            signer="string",
            timestamp=0
        ),
        signature="string"
    ),
    timestamp=1
)

create_event_2_out = EventOut(
    request=Request(
        state=State(
            subject_id="string",
            payload=Payload(
                json_={
                    "foo": "bar"
                }
            )
        )
    ),
    signature=Signature(
        content=ContentSignature(
            event_content_hash="string",
            signer="string",
            timestamp=0
        ),
        signature="string"
    ),
    timestamp=2
)

event_1_in_schema = {
    "request": {
        "Create": {
            "governance_id": "string",
            "namespace": "string",
            "payload": {
                "Json": {"foo": "bar"}
            },
            "schema_id": "string"
        }
    },
    "request_id": "string",
    "sn": 0,
    "subject_id": "string",
    "timestamp": 0
}

event_2_in_schema = {
    "request": {
        "State": {
            "subject_id": "string",
            "payload": {
                "Json": {
                    "foo": "bar"
                }
            },
        }
    },
    "request_id": "JpxalqMTQcDcLG3dwb8uvcrstJo6pmFEzUwhzi0nGPOA",
    "sn": 0,
    "subject_id": "J7BgD3dqZ8vO4WEH7-rpWIH-IhMqaSDnuJ3Jb8K6KvL0",
    "timestamp": 1671705355
}


event_1_in = EventIn(
    request=Request(
        create=Create(
            governance_id="string",
            namespace="string",
            payload=Payload(
                json_={
                    "foo": "bar"
                }
            ),
            schema_id="string"
        )
    ),
    request_id="string",
    sn=0,
    subject_id="string",
    timestamp=0
)

event_2_in = EventIn(
    request=Request(
        state=State(
            subject_id="string",
            payload=Payload(
                json_={
                    "foo": "bar"
                }
            )
        )
    ),
    request_id="JpxalqMTQcDcLG3dwb8uvcrstJo6pmFEzUwhzi0nGPOA",
    sn=0,
    subject_id="J7BgD3dqZ8vO4WEH7-rpWIH-IhMqaSDnuJ3Jb8K6KvL0",
    timestamp=1671705355
)


@pytest.fixture
def get_event_1_out_schema():
    return create_event_1_out_schema


@pytest.fixture
def get_event_2_out_schema():
    return create_event_2_out_schema


@pytest.fixture
def get_event_1_out():
    return create_event_1_out


@pytest.fixture
def get_event_2_out():
    return create_event_2_out


@pytest.fixture
def get_event_1_in():
    return event_1_in


@pytest.fixture
def get_event_2_in():
    return event_2_in


@pytest.fixture
def get_event_1_in_schema():
    return event_1_in_schema


@pytest.fixture
def get_event_2_in_schema():
    return event_2_in_schema


approval_out_schema_1 = {
    "approvalType": "Accept"
}

approval_out_schema_2 = {
    "approvalType": "Reject"
}

approval_out_1 = ApprovalResponse(
    approvalType=ApprovalType.Accept
)

approval_out_2 = ApprovalResponse(
    approvalType=ApprovalType.Reject
)


@pytest.fixture
def get_approval_out_schema_1():  # pylint: disable=missing-function-docstring
    return approval_out_schema_1


@pytest.fixture
def get_approval_out_schema_2():  # pylint: disable=missing-function-docstring
    return approval_out_schema_2


@pytest.fixture
def get_approval_out_1():  # pylint: disable=missing-function-docstring
    return approval_out_1


@pytest.fixture
def get_approval_out_2():  # pylint: disable=missing-function-docstring
    return approval_out_2


approval_1_schema = {
    "approvals": [
        {
            "content": {
                "approval_type": "Accept",
                "event_request_hash": "string",
                "expected_sn": 0,
                "signer": "string",
                "timestamp": 0
            },
            "signature": "string"
        }
    ],
    "request": {
        "Create": {
            "governance_id": "string",
            "namespace": "string",
            "payload": {
                "Json": {"foo": "bar"}
            },
            "schema_id": "string"
        }
    },
    "signature": {
        "content": {
            "event_content_hash": "string",
            "signer": "string",
            "timestamp": 0
        },
        "signature": "string"
    },
    "timestamp": 0
}

approval_2_schema = {
    "approvals": [],
    "request": {
        "State": {
            "payload": {
                "Json": {"foo": "bar"}
            },
            "subject_id": "J7BgD3dqZ8vO4WEH7-rpWIH-IhMqaSDnuJ3Jb8K6KvL0"
        }
    },
    "signature": {
        "content": {
            "event_content_hash": "JhEnzFVF1a-u-rH34cix2A_OXgcfesM6HGOyk7wdrGHk",
            "signer": "EFXv0jBIr6BtoqFMR7G_JBSuozRc2jZnu5VGUH2gy6-w",
            "timestamp": 1671709394
        },
        "signature": "SEnUJq3Y1lbmijKzrc0kuLu-FgMTCyo5PWfDrbi_80bspghCny8Yuvifsmdqq0TjfTUS7sEwmOLir1W_1zeIVyDQ"
    },
    "timestamp": 1671709394
}


approval_1 = EventRequest(
    approvals=[
        Approval(
            content=ContentApproval(
                approval_type=ApprovalType.Accept,
                event_request_hash="string",
                expected_sn=0,
                signer="string",
                timestamp=0
            ),
            signature="string"
        )
    ],
    request=Request(
        create=Create(
            governance_id="string",
            namespace="string",
            payload=Payload(
                json_={
                    "foo": "bar"
                }
            ),
            schema_id="string"
        )
    ),
    signature=Signature(
        content=ContentSignature(
            event_content_hash="string",
            signer="string",
            timestamp=0
        ),
        signature="string"
    ),
    timestamp=0
)

approval_2 = EventRequest(
    approvals=[],
    request=Request(
        state=State(
            payload=Payload(
                json_={
                    "foo": "bar"
                }
            ),
            subject_id="J7BgD3dqZ8vO4WEH7-rpWIH-IhMqaSDnuJ3Jb8K6KvL0"
        )
    ),
    signature=Signature(
        content=ContentSignature(
            event_content_hash="JhEnzFVF1a-u-rH34cix2A_OXgcfesM6HGOyk7wdrGHk",
            signer="EFXv0jBIr6BtoqFMR7G_JBSuozRc2jZnu5VGUH2gy6-w",
            timestamp=1671709394
        ),
        signature="SEnUJq3Y1lbmijKzrc0kuLu-FgMTCyo5PWfDrbi_80bspghCny8Yuvifsmdqq0TjfTUS7sEwmOLir1W_1zeIVyDQ"
    ),
    timestamp=1671709394
)


@pytest.fixture
def get_approval_1_schema():  # pylint: disable=missing-function-docstring
    return approval_1_schema


@pytest.fixture
def get_approval_2_schema():  # pylint: disable=missing-function-docstring
    return approval_2_schema


@pytest.fixture
def get_approval_1():  # pylint: disable=missing-function-docstring
    return approval_1


@pytest.fixture
def get_approval_2():  # pylint: disable=missing-function-docstring
    return approval_2
