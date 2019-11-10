from enum import Enum


class EventType(Enum):
    WORKSHOP = 'Workshop'
    TABLING = 'Tabling'
    CELEBRATION = 'Celebration'
    DROPIN = 'Drop-in center'
    OTHER = 'Other'


class EventApprovalStatus(Enum):
    PENDING = 'Pending'
    APPROVED = 'Approved'

class Languages(Enum):
    ENGLISH = "English"
    SPANISH = "Spanish"
    VIETNAMESE = "Vietnamese"
    CHINESE = "Chinese"
    TAGALOG = "Tagalog"