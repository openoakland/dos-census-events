import csv

from django.forms.models import model_to_dict
from django.http import StreamingHttpResponse
from django.shortcuts import render

from . import models


# https://docs.djangoproject.com/en/2.2/howto/outputting-csv/#streaming-csv-files
class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def export_events(request):
    '''
    Bulk export as CSV of events.
    '''
    fields = [
        'title',
        'start_datetime',
        'end_datetime',
        'location',
        'lat',
        'lon',
        'description',
    ]

    print(models.Event)
    events = models.Event.objects.all()
    pseudo_buffer = Echo()
    writer = csv.DictWriter(pseudo_buffer, fieldnames=fields, dialect='excel')
    response = StreamingHttpResponse((writer.writerow(model_to_dict(event, fields=fields)) for event in events),
                                     content_type="text/csv")

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
        form = EventForm()

    return render(request, 'event.html', {'form': form})
