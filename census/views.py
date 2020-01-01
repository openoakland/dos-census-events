import csv
import io
import json
from datetime import datetime
from itertools import groupby

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, UpdateView
from pytz import timezone

from . import constants, models
from .forms import EditEventForm, EventForm
from .google_calendar import google_publish_event, google_delete_event

# TODO: Timezone has been set to America/Los_Angeles, but maybe we should
#       fetch it from the user's browser settings?
current_timezone = timezone(settings.TIME_ZONE)


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

class HomepageView(View):
    template_name = 'index.html'

    def get(self, request):
        """
        Homepage
        """
        if request.is_ajax():
            # We expect AJAX calls made from datepicker
            return self.get_event_dates(request)
        else:
            request.events = self.make_events_data_response(self.get_events(request))
            request.has_events = bool(request.events)
            if request.GET.dict().get('search'):
                request.search_query = request.GET.dict().get('search').strip()
            else:
                request.search_query = None
            return render(request, self.template_name)

    def get_event_dates(self, request):
        """
        Given a request object, retrieve events matching the criteria specified
        and return only dates.

        :param request: Request object
        :return: HttpResponse object containing list of unique days on which
                 events occur
        """
        events = self.get_events(request)
        dates = set()
        for event in events:
            localized_start_datetime = event.start_datetime.astimezone(current_timezone)
            # %-d removes the leading 0 for single digit dates
            day_of_month = datetime.strftime(localized_start_datetime, "%-d")
            dates.add(day_of_month)
        return HttpResponse(json.dumps(dict(dates=list(dates))))

    def get_events(self, data):
        """
        Given a request object, extract the filter criteria from it and
        retrieve matching events.

        :param data: Request object
        :return: QuerySet object containing event data.
        """
        filter_args = dict()
        if data.GET.dict():
            query_params = self.get_valid_params(data.GET.dict())
            if query_params.get('search'):
                filter_args['search'] = query_params.get('search')
            if query_params.get('isMonthly'):
                # Fetch events for the whole month
                # TODO: Test to ensure that timezone differences are properly accounted for
                #       when using the `__month` filter
                filter_args['month'] = query_params['month']
                filter_args['year'] = query_params['year']
            elif all (key in query_params for key in ('day', 'month', 'year')):
                # Fetch events for a selected date
                day = query_params['day']
                month = query_params['month']
                year = query_params['year']
                start_date = datetime.strptime(f"{year}-{month}-{day} 00:00:00",
                                               "%Y-%m-%d %H:%M:%S")
                end_date = datetime.strptime(f"{year}-{month}-{day} 23:59:59",
                                             "%Y-%m-%d %H:%M:%S")

                filter_args['start_date'] = start_date
                filter_args['end_date'] = end_date
        if not filter_args.get('month'):
            # If no payload is passed to the request, simply fetch current and
            # future approved events
            # filter_args['start_date'] = datetime.now().replace(hour=0, minute=0, second=0)
            # filter_args['end_date'] = datetime.now() + timedelta(days=7)
            filter_args['month'] = datetime.now().month
            filter_args['year'] = datetime.now().year
        filter_args['user_auth_status'] = data.user.is_authenticated
        return self.fetch_events_from_db(**filter_args)

    def get_valid_params(self, query_params):
        """
        Validate URL Query parameters and convert them to Python friendly values where applicable.
        Invalid query parameters/values will be ignored.

        :param query_params: Dictionary containing query parameters and corresponding values.
        :return: Dictionary containing only valid parameters
        """
        valid_params = {}
        for param in query_params:
            if param == 'day' and query_params['day'].isdigit():
                valid_params['day'] = int(query_params['day'])
            elif param == 'month' and query_params['month'].isdigit():
                valid_params['month'] = int(query_params['month'])
            elif param == 'year' and query_params['year'].isdigit():
                valid_params['year'] = int(query_params['year'])
            elif param == 'search' \
                    and query_params['search'] \
                    and not query_params['search'].strip() == "":
                valid_params['search'] = query_params['search'].strip()
            elif param == 'isMonthly':
                if query_params['isMonthly'] == 'true':
                    valid_params['isMonthly'] = True
                elif query_params['isMonthly'] == 'false':
                    valid_params['isMonthly'] = False
        return valid_params

    def fetch_events_from_db(self, **kwargs):
        """
        Retrieve matching approved events data.

        :param kwargs: Arguments containing DB fields and values
        :return: Query set of matching events
        """

        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        month = kwargs.get('month')
        year = kwargs.get('year')
        search = kwargs.get('search')
        user_auth_status = kwargs.get('user_auth_status')

        if not user_auth_status:
            query = Q(approval_status=constants.EventApprovalStatus.APPROVED,
                           is_private_event=0)
        else:
            query = Q(approval_status=constants.EventApprovalStatus.APPROVED)

        if (bool(start_date) ^ bool(end_date)) or (bool(month) ^ bool(year)):
            # If start date is provided but not end date, or vice-versa, raise error
            # Month and year should also both be provided or not at all.
            raise Exception
        if month:
            query = query & Q(start_datetime__month=month, start_datetime__year=year)
        if start_date and end_date:
            query = query & Q(start_datetime__range=(current_timezone.localize(start_date),
                                                     current_timezone.localize(end_date)))
        if search:
            query = query & (Q(title__icontains=search) | Q(description__icontains=search))

        return models.Event.objects.filter(query).order_by('start_datetime')

    def make_events_data_response(self, events):
        """
        Construct the event response object. Events are grouped by start date to simplify
        iterating through the object to display on the landing page.

        :param events: list of Event queryset objects
        :return: Response object with the following format:
        [
            start_date1: [event_dict1, event_dict2],
            start_date2: [event_dict3, event_dict4],
        ]
        """
        result_set = []
        parsed_events = [self.parse_event_queryset(event) for event in events]
        for date, event_data in groupby(parsed_events, key=lambda row: row['start_date']):
            date_to_display = datetime.strptime(date, '%Y-%m-%d').strftime('%A, %B %d')
            result_set.append((date_to_display, list(event_data)))
        return result_set

    def parse_event_queryset(self, event):
        """
        Given an Event object, return a dictionary containing only those attributes
        that are required to be displayed.

        Note: Django provides a Serializer class which we could use here to simplify
        things. However, for security considerations, we still probably only want to
        return attributes that are necessary for front-end display as opposed to the
        whole model.

        :param event: Event objects
        :return: A dictionary representation of the event
        """
        localized_start_datetime = event.start_datetime.astimezone(current_timezone)
        localized_end_datetime = event.end_datetime.astimezone(current_timezone)
        start_date = datetime.strftime(localized_start_datetime, "%Y-%m-%d")
        end_date = datetime.strftime(localized_end_datetime, "%Y-%m-%d")
        start_time = datetime.strftime(localized_start_datetime, "%I:%M %p")
        end_time = datetime.strftime(localized_end_datetime, "%I:%M %p")
        return dict(id=event.id,
                    title=event.title,
                    description=event.description,
                    month=localized_start_datetime.month,
                    is_private_event=event.is_private_event,
                    start_date=start_date,
                    end_date=end_date,
                    start_time=start_time,
                    end_time=end_time,
                    )


class SubmitEventView(View):
    template_name = 'census/event_form.html'

    def get(self, request, *args, **kwargs):
        tz = timezone(settings.TIME_ZONE)
        form = EventForm(initial={
            'languages': [constants.Languages.ENGLISH],
            'start_datetime': datetime.today().astimezone(tz).replace(hour=18, minute=0, second=0, microsecond=0),
            'end_datetime': datetime.today().astimezone(tz).replace(hour=19, minute=0, second=0, microsecond=0),
        })

        enable_recurrence = request.GET.get('enable_recurrence', False)
        return render(request, self.template_name, {
            'form': form,
            'enable_recurrence': enable_recurrence,
        })


    def post(self, request, *args, **kwargs):
        # create a form instance and populate it with data from the request:
        form = EventForm(request.POST)
        message = ''

        # check whether it's valid:
        if form.is_valid():
            form.save()
            message =request.POST['title'] + " successfully created."
            status_code = 201
            form = EventForm(initial={
                'languages': [constants.Languages.ENGLISH],
                'start_datetime': datetime.today().replace(hour=18, minute=0, second=0, microsecond=0),
                'end_datetime': datetime.today().replace(hour=19, minute=0, second=0, microsecond=0),
            })
        else:
            status_code = 400

        return render(
            request,
            self.template_name,
            {'form': form, 'message': message},
            status=status_code,
        )


class UpdateEvent(LoginRequiredMixin, UpdateView):
    model = models.Event
    login_url = '/login/'
    form_class = EditEventForm
    template_name = 'census/event_form.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.prev_status = self.object.approval_status
        return super().post(request, *args, **kwargs)

    # If the status before the update was APPROVED then go to the approved list.
    def get_success_url(self):
        if self.prev_status == constants.EventApprovalStatus.APPROVED:
            return "/approved"
        return "/pending"
    # Override the form_valid method to push event to google calendar
    def form_valid(self, form):
        self.object = form.save()
        if form.instance.approval_status == constants.EventApprovalStatus.APPROVED:
            google_publish_event(form.instance)
        return HttpResponseRedirect(self.get_success_url())

class PendingList(ListView):
    model = models.Event
    queryset = models.Event.objects.filter(approval_status = constants.EventApprovalStatus.PENDING)
    template_name = 'census/pending_list.html'

class ApprovedList(ListView):
    model = models.Event
    queryset = models.Event.objects.filter(approval_status = constants.EventApprovalStatus.APPROVED)
    template_name = 'census/approved_list.html'

class DeleteEvent(LoginRequiredMixin, DeleteView):
    model = models.Event
    login_url = '/login/'
    # Override the delete method so we can delete for the google calendar
    def delete(self, request, *args, **kwargs):
        self.object = event = self.get_object()
        google_delete_event(event)
        event.delete()
        # Return to the list we came from.
        if event.approval_status == constants.EventApprovalStatus.APPROVED:
            return HttpResponseRedirect("/approved")
        else:
            return HttpResponseRedirect("/pending")

class ShowEvent(UpdateView):
    model = models.Event
    form_class = EditEventForm
    template_name = 'census/event_form.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['readonly'] = 'readonly'
        return context
