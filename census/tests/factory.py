"""
Factory methods to help with creating valid test data.
"""

from datetime import datetime

from pytz import timezone

from census import constants
from census.models import Event


def event(**kwargs):
    data = dict(
        title="OpenOakland Day of Service",
        description="Single day event engaing community and technology",
        organization_name="OpenOakland",
        location="Oakland City Hall",
        event_type=constants.EventType.WORKSHOP,
        start_datetime=datetime(2019, 11, 5, 18, 0, tzinfo=timezone('America/Los_Angeles')),
        end_datetime=datetime(2019, 11, 5, 21, 0, tzinfo=timezone('America/Los_Angeles')),
        recurrences=[],
        approval_status=constants.EventApprovalStatus.APPROVED,
        languages=[constants.Languages.ENGLISH],
    )

    data.update(kwargs)

    return Event(**data)
