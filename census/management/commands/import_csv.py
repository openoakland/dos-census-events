from typing import List

import logging, csv, argparse
from datetime import datetime, timedelta
from pytz import timezone
from recurrence import Recurrence

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from census.models import Event
from census import constants

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
tz = timezone(settings.TIME_ZONE)

EVENT_TYPE = constants.EventType.QAC
approval_status = constants.EventApprovalStatus.APPROVED
LANGUAGES = [lang[1] for lang in constants.language_choices]
START_DATE = datetime(year=2020, month=3, day=12)
END_DATE = datetime(year=2020, month=5, day=12)

def is_valid(row: List):
    # Validates that the row contains all the necessary data
    return bool(get_title(row).replace(" Questionnaire Assistance Center", "")) and \
        bool(get_location(row)) and \
        bool(get_city(row)) and \
        bool(get_zip(row))
        # bool(get_(row))

def get_title(row: List):
    return "Questionnaire Assistance Center"

def get_location(row: List):
    return row[5]

def get_site_name(row: List):
    return row[4]

def get_city(row: List):
    return row[6]

def get_zip(row: List):
    return row[7]

def get_phone_number(row: List):
    return row[8]

def get_contact(row: List):
    return None

def get_email(row: List):
    return None
    
def get_description(row: List):
    return row[22]

def get_times(row: List):
    return [
        get_monday(row),
        get_tuesday(row),
        get_wednesday(row),
        get_thursday(row),
        get_friday(row),
        get_saturday(row),
        get_sunday(row)
    ]

def get_datetimes(times: List, start_day: datetime, end_day: datetime) -> List:
    event_datetimes = []
    day_count = (end_day - start_day).days + 1
    for day in [start_day + timedelta(days=n) for n in range(day_count)]:
        start_time = times[day.weekday()][0]
        end_time = times[day.weekday()][1]
        if not start_time or not end_time:
            continue
        start_datetime = datetime(
            year=day.year, month=day.month, day=day.day, hour=start_time.hour, minute=start_time.minute
            ).astimezone(tz)
        end_datetime = datetime(
            year=day.year, month=day.month, day=day.day, hour=end_time.hour, minute=end_time.minute
            ).astimezone(tz)
        event_datetimes.append(
            (start_datetime, end_datetime)    
        )
    return event_datetimes

def get_monday(row: List):
    time_frame = row[15]
    start_time = get_start_time(time_frame)
    end_time = get_end_time(time_frame)
    if not start_time or not end_time:
        return None, None
    else:
        return start_time, end_time

def get_tuesday(row: List):
    time_frame = row[16]
    start_time = get_start_time(time_frame)
    end_time = get_end_time(time_frame)
    if not start_time or not end_time:
        return None, None
    else:
        return start_time, end_time

def get_wednesday(row: List):
    time_frame = row[17]
    start_time = get_start_time(time_frame)
    end_time = get_end_time(time_frame)
    if not start_time or not end_time:
        return None, None
    else:
        return start_time, end_time

def get_thursday(row: List):
    time_frame = row[18]
    start_time = get_start_time(time_frame)
    end_time = get_end_time(time_frame)
    if not start_time or not end_time:
        return None, None
    else:
        return start_time, end_time

def get_friday(row: List):
    time_frame = row[19]
    start_time = get_start_time(time_frame)
    end_time = get_end_time(time_frame)
    if not start_time or not end_time:
        return None, None
    else:
        return start_time, end_time

def get_saturday(row: List):
    time_frame = row[20]
    start_time = get_start_time(time_frame)
    end_time = get_end_time(time_frame)
    if not start_time or not end_time:
        return None, None
    else:
        return start_time, end_time

def get_sunday(row: List):
    time_frame = row[21]
    start_time = get_start_time(time_frame)
    end_time = get_end_time(time_frame)
    if not start_time or not end_time:
        return None, None
    else:
        return start_time, end_time


def get_start_time(time_frame: str):
    if "-" not in time_frame:
        logger.debug(f"Can't parse {time_frame}")
        return None
    start_time = time_frame.split("-")[0].strip()
    return parse_time(start_time)

def get_end_time(time_frame: str):
    if "-" not in time_frame:
        logger.debug(f"Can't parse {time_frame}")
        return None
    end_time = time_frame.split("-")[1].strip()
    return parse_time(end_time)

def parse_time(time_str: str):
    try:
        result = datetime.strptime(time_str, "%I:%M%p")
    except ValueError:
        logger.debug(f"Can't parse {time_str}")
        result = None
    return result



def get_languages(row: List):
    # English is to be included by default
    english = constants.Languages.ENGLISH
    # languages_input = row[30]
    languages_input = []
    if not languages_input:
        return [english]

    # The languages input can be seperated by 
    # "/", "," or nothing when only one language
    if "/" in languages_input:
        languages_input = languages_input.split("/")
    elif ", " in languages_input:
        languages_input = languages_input.split(", ")
    else:
        # languages_input is a single language
        languages_input = [languages_input]

    languages = [english] + languages_input
    return languages

def get_ada_compliance(row: List):
    is_compliant = row[26]
    return is_compliant.lower() == "yes"

def get_organization_name(row: List):
    return row[4]


def parse_date(date: str):
    try:
        return datetime.strptime(date, "%m-%d-%Y")
    except ValueError:
        return datetime.strptime(date, "%m/%d/%Y")


def get_start_date(row: List):
    date_str = row[13]
    try:
        return parse_date(date_str)
    except ValueError:
        logger.debug(f"Defaulting start for {get_site_name(row)}")
        return START_DATE

def get_end_date(row: List):
    date_str = row[14]
    try:
        return parse_date(date_str)
    except ValueError:
        logger.debug(f"Defaulting end for {get_site_name(row)}")
        return END_DATE

def date_type(value):
    return datetime.strptime(value, "%m-%d-%Y")

def hash_event(event):
    return f"{event.title} || {event.start_datetime.astimezone(timezone('UTC'))} || {event.end_datetime.astimezone(timezone('UTC'))} || {event.location}"

def get_existing_events_lookup():
    # returns a lookup of events
    return {
        hash_event(event) for event in Event.objects.all()
    }

class Command(BaseCommand):
    help = 'Creates Events from csv file.'

    # def add_arguments(self, parser):
    #     parser.add_argument('--start_date', required=True, type=date_type, 
    #         help="Start date of events, format MM-DD-YYYY")
        
    #     parser.add_argument('--end_date', required=True, type=date_type, 
    #         help="Last date of events, format MM-DD-YYYY")


    def handle(self, *args, **options):
        events = []
        existing_events = get_existing_events_lookup()
        with open("census_events.csv", "r") as file:
            reader = csv.reader(file)
            header = next(reader)
            next(reader) # second row is used to indicate if should store info for that column
            for i, row in enumerate(reader):
                if not is_valid(row):
                    logger.debug(f"Row {i} failed to validate")
                    continue
                title = get_title(row)
                location = get_location(row)
                site_name = get_site_name(row)
                city = get_city(row)
                zip_code = get_zip(row)
                phone_number = get_phone_number(row)
                contact = get_contact(row)
                email = get_email(row)
                description = get_description(row)
                organization_name = get_organization_name(row)
                is_ada_compliant = get_ada_compliance(row)
                languages = get_languages(row)
                for lang in languages:
                    if lang not in LANGUAGES:
                        print(f"{lang} missing")

                start_date = get_start_date(row)
                end_date = get_end_date(row)

                # languages = []
                times = get_times(row)
                times = get_datetimes(times, start_date, end_date)
                for start, end in times:
                    event = Event(title=title, description=description, start_datetime=start, end_datetime=end, 
                        location=location, site_name=site_name, city=city, zip_code=zip_code, 
                        event_type=EVENT_TYPE, is_census_equipped=True, approval_status=approval_status, 
                        languages=languages, contact_name=contact, contact_email=email, contact_phone=phone_number,
                        is_ada_compliant=is_ada_compliant, organization_name=organization_name, recurrences=Recurrence())
                    if hash_event(event) not in existing_events:
                        events.append(event)
                    else:
                        logger.debug("This event already exists!")
        

        logger.info(f"Num events before: {Event.objects.count()}")
        Event.objects.bulk_create(events)
        logger.info(f"Num events after: {Event.objects.count()}")
        logger.info(f"Created {len(events)} events")