import csv
from datetime import datetime, timedelta
import io
from itertools import groupby
import json

from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from pytz import timezone

from . import constants, models
from .forms import EditEventForm, EventForm

# TODO: Timezone has been set to US/Pacific, but we should probably
#       fetch it from the users's browser
TIMEZONE = 'US/Pacific'

def export_events(request):
    '''
    Bulk export as CSV of events.
    '''
    fields = [
        'title',
        'recurrences',
        'start_datetime',
        'end_datetime',
        'location',
        'lat',
        'lon',
        'description',
    ]

    events = models.Event.objects.all()
    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=fields, dialect='excel')

    # Create a generator that writes to an in-memory CSV buffer in rows of 1000
    # at a time. This allows us to stream a very large number of events to the
    # browser.
    def events_of(size=1000):
        writer.writeheader()
        i = 0
        for event in events:
            writer.writerow(model_to_dict(event, fields=fields))
            if i % size == (size - 1):
                yield csv_buffer.getvalue()
                csv_buffer.truncate(0)
                csv_buffer.seek(0)
            i += 1

        yield csv_buffer.getvalue()

    response = StreamingHttpResponse(events_of(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="census_events.csv"'
    return response


def index(request):
    """
    Homepage
    """
    return render(request, 'index.html')


def get_events(data):
    """
    This endpoint /events is called by the datepicker (census/static/datepicker/js/datepicker.js)
    to retrieve a list of filtered events by selected date/month.

    :param data: Request object
    :return: HttpResponse object containing event data. Populate
    """
    query_params = data.GET.dict()
    if not query_params:

        # If no payload is passed to the request, simply fetch future approved events
        start_date = datetime.now(timezone(TIMEZONE))

        # TODO: When the user first visits the homepage, all events occurring
        #      in the week are fetched. Should this be changed instead to display
        #      only events for the current day?
        end_date = datetime.now(timezone(TIMEZONE)) + timedelta(days=7)

        events = models.Event.objects.filter(approval_status=constants.EventApprovalStatus.APPROVED.name,
                                             start_datetime__range=(start_date, end_date))\
                                      .order_by('start_datetime')
        return HttpResponse(json.dumps(make_events_data_response(events)))

    if 'isMonthly' in query_params and query_params['isMonthly'] == 'true':
        # Fetch events for the whole month

        month = int(query_params['month'])

        # TODO: Ensure that timezone differences are properly accounted for
        #       when using the `__month` filter
        events = models.Event.objects.filter(approval_status=constants.EventApprovalStatus.APPROVED.name,
                                             start_datetime__month=month)\
                                     .order_by('start_datetime')
        return HttpResponse(json.dumps(make_events_data_response(events)))

    else:
        # Fetch events for a selected date
        day = query_params['day']
        month = query_params['month']
        year = query_params['year']
        start_date = datetime.strptime(f"{year}-{month}-{day} 00:00:00", "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(f"{year}-{month}-{day} 23:59:59", "%Y-%m-%d %H:%M:%S")

        current_timezone = timezone(TIMEZONE)
        events = models.Event.objects.filter(approval_status=constants.EventApprovalStatus.APPROVED.name,
                                             start_datetime__range=(current_timezone.localize(start_date),
                                                                    current_timezone.localize(end_date))) \
            .order_by('start_datetime')
        return HttpResponse(json.dumps(make_events_data_response(events)))


def make_events_data_response(events):
    result_set = {}
    parsed_events = [parse_event_queryset(event) for event in events]
    for month, event_data in groupby(parsed_events, key=lambda row: row['month']):
        result_set[int(month)] = list(event_data)
    return dict(events=result_set)


def parse_event_queryset(event):
    """
    Given an Event object, return a dictionary containing only those attributes
    that are required to be displayed.

    :param event: Event objects
    :return: A dictionary representation of the event
    """

    localized_start_datetime = event.start_datetime.astimezone(timezone(TIMEZONE))
    start_date = datetime.strftime(localized_start_datetime, "%Y-%m-%d")
    end_date = datetime.strftime(localized_start_datetime, "%Y-%m-%d")
    month = datetime.strftime(localized_start_datetime, "%m")
    start_time = datetime.strftime(localized_start_datetime, "%I:%M %p")
    end_time = datetime.strftime(localized_start_datetime, "%I:%M %p")
    return dict(id=event.id,
                title=event.title,
                description=event.description,
                month=month,
                start_date=start_date,
                end_date=end_date,
                start_time=start_time,
                end_time=end_time,
                )


class SubmitEventView(View):
    template_name = 'event.html'

    def get(self, request, *args, **kwargs):
        form = EventForm(initial={
            'languages': [constants.Languages.ENGLISH.name],
            'start_datetime': datetime.today().replace(hour=18, minute=0, second=0, microsecond=0),
            'end_datetime': datetime.today().replace(hour=19, minute=0, second=0, microsecond=0),
        })

        enable_recurrence = request.GET.get('enable_recurrence', False)
        return render(request, self.template_name, {
            'form': form,
            'enable_recurrence': enable_recurrence,
        })


    def post(self, request, *args, **kwargs):
        # create a form instance and populate it with data from the request:
        form = EventForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            form.save()
            status_code = 201
        else:
            status_code = 400

        return render(
            request,
            self.template_name,
            {'form': form},
            status=status_code,
        )


class UpdateEvent(LoginRequiredMixin, UpdateView):
    model = models.Event
    success_url = "/pending"
    login_url = '/login/'
    form_class = EditEventForm

class PendingList(ListView):
    model = models.Event
    queryset = models.Event.objects.filter(approval_status = constants.EventApprovalStatus.PENDING.name)
    template_name = 'census/pending_list.html'

class DeleteEvent(LoginRequiredMixin, DeleteView):
    model = models.Event
    success_url = "/pending"
    login_url = '/login/'
