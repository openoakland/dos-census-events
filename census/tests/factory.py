"""
Factory methods to help with creating valid test data.
"""

from datetime import datetime
import uuid

from pytz import timezone

from census import constants
from census.models import Event, GoogleEvent


def event(**kwargs):
    data = dict(
        title="OpenOakland Day of Service",
        description="Single day event engaing community and technology",
        organization_name="OpenOakland",
        location="Oakland City Hall",
        event_type=constants.EventType.WORKSHOP,
        start_datetime=datetime(2019, 11, 5, 18, 0, 0, 0, timezone('America/Los_Angeles')),
        end_datetime=datetime(2019, 11, 5, 21, 0, 0, 0, timezone('America/Los_Angeles')),
        recurrences=[],
        approval_status=constants.EventApprovalStatus.APPROVED,
        languages=[constants.Languages.ENGLISH],
    )

    data.update(kwargs)

    return Event(**data)


def google_event(**kwargs):
    # If you see this error when saving the GoogleEvent:
    #
    # > django.db.utils.IntegrityError: NOT NULL constraint failed: census_googleevent.event_id
    #
    # Create an Event using the event factory, save it, then supply it to the
    # GoogleEvent factory. Django OneToOne models require that the related
    # model exists before saving. Maybe there is a better way to handle this.
    data = dict(
        google_calendar_id=uuid.uuid4(),
        event=event(),
        published=datetime(2019, 11, 16, 14, 53, 27).astimezone(timezone('America/Los_Angeles')),
    )

    data.update(kwargs)

    return GoogleEvent(**data)
