from enum import Enum


class EventType:
    WORKSHOP = 'Workshop'
    TABLING = 'Tabling'
    CELEBRATION = 'Celebration'
    DROPIN = 'Drop-in center'
    OTHER = 'Other'

event_type_choices = (
    (EventType.WORKSHOP, EventType.WORKSHOP),
    (EventType.TABLING, EventType.TABLING),
    (EventType.CELEBRATION, EventType.CELEBRATION),
    (EventType.DROPIN, EventType.DROPIN),
    (EventType.OTHER, EventType.OTHER),
)


class EventApprovalStatus:
    PENDING = 'Pending'
    APPROVED = 'Approved'

approval_status_choices = (
    (EventApprovalStatus.PENDING, EventApprovalStatus.PENDING),
    (EventApprovalStatus.APPROVED, EventApprovalStatus.APPROVED),
)

class Languages:
    ENGLISH = "English"
    SPANISH = "Spanish"
    VIETNAMESE = "Vietnamese"
    CHINESE = "Chinese"
    TAGALOG = "Tagalog"

language_choices = (
    (Languages.ENGLISH, Languages.ENGLISH),
    (Languages.SPANISH, Languages.SPANISH),
    (Languages.VIETNAMESE, Languages.VIETNAMESE),
    (Languages.CHINESE, Languages.CHINESE),
    (Languages.TAGALOG, Languages.TAGALOG),
)