from enum import Enum


class EventType:
    QAC = 'Questionnaire Assistance Center'
    INFO = 'Information Booth'
    MEETING = 'Informational Meeting'
    WORKSHOP = 'Census Completion Workshop'
    TOWNHALL = 'Town Hall'
    PARTY = 'Block Party'
    WEBINAR = 'Webinar'
    OTHER = 'Other'

event_type_choices = (
    (EventType.QAC, EventType.QAC),
    (EventType.INFO, EventType.INFO),
    (EventType.MEETING, EventType.MEETING),
    (EventType.WORKSHOP, EventType.WORKSHOP),
    (EventType.TOWNHALL, EventType.TOWNHALL),
    (EventType.PARTY, EventType.PARTY),
    (EventType.WEBINAR, EventType.WEBINAR),
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
    MANDARIN = "Mandarin"
    CANTONESE = "Cantonese"
    TAGALOG = "Tagalog"
    HINDI = "Hindi"
    VIETNAMESE = "Vietnamese"
    PUNJABI = "Punjabi"
    TAMIL = "Tamil"
    TELUGU = "Telugu"
    KOREAN = "Korean"
    ARABIC = "Arabic"
    FARSI = "Farsi"
    DARI = "Dari"

language_choices = (
    (Languages.ENGLISH, Languages.ENGLISH),
    (Languages.SPANISH, Languages.SPANISH),
    (Languages.MANDARIN, Languages.MANDARIN),
    (Languages.CANTONESE, Languages.CANTONESE),
    (Languages.TAGALOG, Languages.TAGALOG),
    (Languages.HINDI, Languages.HINDI),
    (Languages.VIETNAMESE, Languages.VIETNAMESE),
    (Languages.PUNJABI, Languages.PUNJABI),
    (Languages.TAMIL, Languages.TAMIL),
    (Languages.TELUGU, Languages.TELUGU),
    (Languages.KOREAN, Languages.KOREAN),
    (Languages.ARABIC, Languages.ARABIC),
    (Languages.FARSI, Languages.FARSI),
    (Languages.DARI, Languages.DARI),
)
