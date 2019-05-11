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
