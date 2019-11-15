import csv
import io

from django.forms.models import model_to_dict
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from . import constants, models


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
    return render(request, 'index.html')

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
        form = EventForm(initial={'languages': [constants.Languages.ENGLISH]})

    selected_languages = []
    # Uncomment the below when languages is no longer excluded from the form
    # selected_languages = [language.name for language in form['languages'].value()]
    
    return render(request, 'event.html', {
        'form': form,
        'selected_languages': selected_languages,
    })

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

