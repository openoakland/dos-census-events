import csv
import io
import json

from django.forms.models import model_to_dict
from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from . import models


def export_events(request):
    '''
    Bulk export as CSV of events.
    '''
    fields = [
        'title',
        'recurrences',
        'start_time',
        'end_time',
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
    # Uncomment this if we need to call the homepage in the future using AJAX
    # if request.is_ajax():
    #     return get_events()
    events = models.Event.objects.all()
    request.events = events
    # current_date = datetime.now()
    # request.events_title = f'{current_date.strftime("%B")} {current_date.strftime("%Y")} Events'
    return render(request, 'index.html')


def get_events(data):
    """
    This endpoint /events is called by the datepicker (census/static/datepicker/js/datepicker.js)
    to retrieve a list of filtered events by selected date/month.

    :param data: Request object
    :return: HttpResponse object containing event data. Populate
    """
    query_params = data.GET.dict()
    if 'isMonthly' in query_params and query_params['isMonthly'] == 'true':
        # get monthly events
        # TODO: Fetch Event objects based on start and end dates
        month = query_params['month']
        return HttpResponse(json.dumps(dict(request={'events': [
            dict(id=4, title='Title4', description='SSS', start_time='123', end_time='433'),
            dict(id=5, title='Title5', description='SSS', start_time='123', end_time='433')
        ]})))
    else:
        # Get events for a selected date
        # TODO: Fetch Event objects based on start and end dates
        day = query_params['day']
        return HttpResponse(json.dumps(dict(request={'events': [
            dict(id=2, title='Title2', description='SSS', start_time='123', end_time='433'),
            dict(id=3, title='Title3', description='SSS', start_time='123', end_time='433')
        ]})))


from .forms import EventForm
from django.http import HttpResponseRedirect

def add_event(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EventForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/submit/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EventForm()

    return render(request, 'event.html', {'form': form})

class UpdateEvent(LoginRequiredMixin, UpdateView):
    model = models.Event
    fields = '__all__'
    success_url = "/pending"
    login_url = '/login/'

class PendingList(ListView):
    model = models.Event
    queryset = models.Event.objects.filter(approval_status = 'PENDING')
    template_name = 'census/pending_list.html'

class DeleteEvent(LoginRequiredMixin, DeleteView):
    model = models.Event
    success_url = "/pending"
    login_url = '/login/'
