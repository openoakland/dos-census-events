from django.utils.translation import gettext as _
from enum import Enum


class EventType(Enum):
    WORKSHOP = _('Workshop')
    TABLING = _('Tabling')
    CELEBRATION = _('Celebration')
    DROPIN = _('Drop-in center')
    OTHER = _('Other')


class EventApprovalStatus(Enum):
    PENDING = _('Pending')
    APPROVED = _('Approved')
