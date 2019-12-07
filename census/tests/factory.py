"""
Factory methods to help with creating valid test data.
"""

from datetime import datetime

import pytz

from census import constants
from census.models import Event

los_angeles = pytz.timezone('America/Los_Angeles')


def event(**kwargs):
    data = dict(
        title="OpenOakland Day of Service",
        description="Single day event engaing community and technology",
        organization_name="OpenOakland",
        location="Oakland City Hall",
        event_type=constants.EventType.WORKSHOP,
        start_datetime=datetime(2019, 11, 5, 18, 0).astimezone(los_angeles),
        end_datetime=datetime(2019, 11, 5, 21, 0).astimezone(los_angeles),
        recurrences=[],
        approval_status=constants.EventApprovalStatus.APPROVED,
        languages=[constants.Languages.ENGLISH],
    )

    data.update(kwargs)

    return Event(**data)
