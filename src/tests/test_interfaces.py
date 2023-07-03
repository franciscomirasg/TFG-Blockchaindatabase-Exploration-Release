import pytest
from pytest_lazyfixture import lazy_fixture

from interfaces.event import Event, EventRequest, Request
from interfaces.request import EventIn
from interfaces.subject import Subject


class TestSubject:
    """
    Test suite for Subject interface.
    """
    @pytest.mark.parametrize(
        "schema, subject",
        [
            (lazy_fixture("get_subject_schema_1"),
             lazy_fixture("get_subject_1")),
            (lazy_fixture("get_subject_schema_2"),
             lazy_fixture("get_subject_2")),
        ]
    )
    def test_http_to_subject(self, schema, subject):
        """
        Test that a subject from rest is correctly converted to a subject object.
        """
        reconstructed_subject = Subject.parse_obj(
            schema
        )
        assert reconstructed_subject == subject

    def test_http_to_all_subjects(self, get_all_subjects_schema, get_all_subjects):
        """
        Test that a list of subjects from rest is correctly converted to a list of subject objects.
        """
        reconstructed_subjects = [Subject.parse_obj(
            schema
        ) for schema in get_all_subjects_schema]
        assert reconstructed_subjects == get_all_subjects


class TestEvent:
    """
    Test suite for Event API interface.
    """

    def test_http_event_properties_create_to_request(self, get_request_create_schema, get_request_create):
        """
        Test that a request from rest is correctly converted to a request object.
        """
        reconstructed_request = Request.parse_obj(
            get_request_create_schema
        )
        assert reconstructed_request == get_request_create

    def test_http_event_properties_state_to_request(self, get_request_state_schema, get_request_state):
        """
        Test that a request from rest is correctly converted to a request object.
        """
        reconstructed_request = Request.parse_obj(
            get_request_state_schema
        )
        assert reconstructed_request == get_request_state

    @pytest.mark.parametrize(
        "schema, event",
        [
            (lazy_fixture("get_event_1_schema"), lazy_fixture("get_event_1")),
            (lazy_fixture("get_event_2_schema"), lazy_fixture("get_event_2")),
        ]
    )
    def test_http_event_to_event(self, schema, event):
        """
        Test that an event from rest is correctly converted to an event object.
        """
        reconstructed_event = Event.parse_obj(
            schema
        )
        assert reconstructed_event == event

    def test_https_events_to_events(self, get_events_schema, get_events):
        """
        Test that a list of events from rest is correctly converted to a list of event objects.
        """
        reconstructed_events = [Event.parse_obj(
            schema
        ) for schema in get_events_schema]
        assert reconstructed_events == get_events

    @pytest.mark.parametrize(
        "schema, event",
        [
            (lazy_fixture("get_event_1_out_schema"),
             lazy_fixture("get_event_1_out")),
            (lazy_fixture("get_event_2_out_schema"),
             lazy_fixture("get_event_2_out")),
        ]
    )
    def test_event_out_to_http(self, schema, event):
        """
        Test that an event object is correctly converted to an event for rest.
        """
        reconstructed_schema = event.to_request()
        assert schema == reconstructed_schema

    @pytest.mark.parametrize(
        "schema, event",
        [
            (lazy_fixture("get_event_1_in_schema"),
             lazy_fixture("get_event_1_in")),
            (lazy_fixture("get_event_2_in_schema"),
             lazy_fixture("get_event_2_in")),
        ]
    )
    def test_http_to_event_in(self, schema, event):
        """
        Test that an event from rest is correctly converted to an event object.
        """
        reconstructed_event = EventIn.parse_obj(
            schema
        )
        assert reconstructed_event == event


class TestApproval:
    """
    Test suite for Approval API interface.
    """

    @pytest.mark.parametrize(
        "schema, approval",
        [
            (lazy_fixture("get_approval_out_schema_1"),
             lazy_fixture("get_approval_out_1")),
            (lazy_fixture("get_approval_out_schema_2"),
             lazy_fixture("get_approval_out_2")),
        ]
    )
    def test_approval_out_to_http(self, schema, approval):
        """
        Test that an approval object is correctly converted to an approval for rest.
        """
        reconstructed_schema = approval.to_request()
        assert schema == reconstructed_schema

    @pytest.mark.parametrize(
        "schema, approval",
        [
            (lazy_fixture("get_approval_1_schema"),
             lazy_fixture("get_approval_1")),
            (lazy_fixture("get_approval_2_schema"),
             lazy_fixture("get_approval_2")),
        ]
    )
    def test_http_to_approval(self, schema, approval):
        """
        Test that an approval from rest is correctly converted to an approval object.
        """
        reconstructed_approval = EventRequest.parse_obj(
            schema
        )
        assert reconstructed_approval == approval
