[![CircleCI](https://circleci.com/gh/openoakland/dos-census-events.svg?style=svg)](https://circleci.com/gh/openoakland/dos-census-events)
# Census events and resources

Find census events and resources near you.


## "Goals"

- Events and resources
- Partners can enter event information through forms
- Events are published to Google Calendar
- Export events via CSV
- Integrate with SwORD via CSV export

Instead of re-creating a calendar tool, we're leveraging a fantastic and proven
one: Google Calendar.


## Usage

Census Events creates a publishing workflow around Google Calendar. Currently,
the publishing is one-way, from Census Events to Google Calendar.

Workflow:
![Worflow Diagram](https://github.com/openoakland/dos-census-events/blob/master/docs/workflow.jpg)

### Setup Google Calendar

Census Events will publish events to Google Calendar. You need to create
a Calendar as well as a [Service
Account](https://developers.google.com/identity/protocols/OAuth2ServiceAccount),
to publish events on your behalf.

1. Make sure you are logged into Google with your G Suite account (you can also
   use your personal account if you don't have a G Suite organization).
1. Create a new [Google API
   Project](https://console.developers.google.com/apis/credentials). Click on
   "My Project" at the top of the page to create a new project.
1. Create a [Service Account](https://console.developers.google.com/iam-admin/serviceaccounts/create)
   for the project. Don't set any roles, they are not necessary.
1. Create a (JSON) key for the Service Account and save the JSON file. Treat
   this file as a secret, please don't commit it to GitHub. This JSON string
   should be provided to the application as the `GOOGLE_SERVICE_ACCOUNT_INFO`
   environment variable. You can edit by hand into a single line or use
   [jq](https://stedolan.github.io/jq/).

       $ jq -c . ./google-service-account.json

1. Enable the [Calendar API](https://console.developers.google.com/apis/api/calendar-json.googleapis.com/overview)
   for the API Project you just created.
1. Create a [Google Calendar](https://calendar.google.com/calendar/r/settings)
   and share the calendar with your Service Account's email address. You can
   find your Service Account's email address in the [IAM
   Admin](https://console.developers.google.com/iam-admin/serviceaccounts).
   Allow the Service Account to "Make changes to events" to your calendar. To
   access sharing settings, open your [Google Calendar
   settings](https://calendar.google.com/calendar/r/settings) and then click the
   calendar you just created from the left navigation under "Settings for my
   calendars".
1. Copy the Calendar Id from the settings in Google Calendar and set the
   environment variable `GOOGLE_CALENDAR_ID`.


### Create calendar events

[Create an event](http://localhost:8000/admin/census/event/add/).


### Configuration

The application is configured through environment variables. You may set these
in `.env` at the project root and they will be loaded automatically. Copy
`env.sample` to `.env` as a template.

Variable | Description | Required | Example
-------- | ----------- | -------- | -------
`ALLOWED_HOSTS` | The list of hostnames to serve requests from. | N | `app.example.com`
`DATABASE_URL` | The connection settings for the database in URL form.  | N | `postgresql://user:password@hostname/db_name?options`
`DJANGO_LOG_LEVEL` | Logging verbosity for django module. | N | `INFO`
`DEBUG` | When true, enable debugging features for development. | N | `1`
`GOOGLE_CALENDAR_ID` | The Google Calendar Id where events will be published. | N | `m7m16tqeokpbreeljd3m2n5jqg@group.calendar.google.com`
`GOOGLE_SERVICE_ACCOUNT_INFO` | JSON string containing your Service Account credentials. | N | `{"type": "service_account", ... }`
`LOG_LEVEL` | Logging verbosity. | N | `INFO`
`SECRET_KEY` | A secret key to provide cryptographic signing for Django. | **Y** | `rHNbX.W^)fw0eS_t]GYm4BsB::Gn?Va8cLA${wtKFvE2RZrR#,`
`TIME_ZONE` | Set the server TZ to your local timezone.  | N | `America/Los_Angeles`


## Development

Thank you for considering a contribution to our project! Follow these
instructions to get setup for development. Read over our
[CONTRIBUTING](./CONTRIBUTING.md) for more information on how we work.


### Prerequisites

- Python 3.6
- pipenv

We assume you are installing to a python virtualenv using pipenv.

Check your versions (optional):

    $ python --version
    $ python3 --version
    $ pip --version
    $ pipenv --version


### Setup

ONLY do this in the dos-census-events directory.
Ensure you are currenty in the project directory.


#### Initialize new project virtualenv and enter the environment shell:

Initialize environment.

    $ pipenv --python 3

Enter environment shell.

    $ pipenv shell

Documentation resource: https://docs.python-guide.org/dev/virtualenvs/

#### Configuration

For development, copy these settings to a `.env` file in the project root
directory.

```
DEBUG=1
DATABASE_URL=sqlite:///db.sqlite3
SECRET_KEY=not-a-secret
```


#### Install the requirements, initialize database and create a super user:

Install python dependencies.

    $ pipenv install --dev

Initialize the database.

    $ python manage.py migrate

Create an admin user by following the prompts.

    $ python manage.py createsuperuser


### Starting the Django server locally:

    $ python manage.py runserver


### Quitting the server and exiting the shell:

Quit the server using CONTROL-C

Exiting the shell using CONTROL-D or

    $ exit


### Working with database migrations

Anytime you make a change to the models, you should try to run makemigrations to
generate a database migration.

    $ python manage.py makemigrations census
    
 ### Resources
- [USWDS CSS Framework](https://designsystem.digital.gov/)
- [Google Calender API Documentation](https://developers.google.com/calendar/)
- [Django 2.2 Documentation](https://docs.djangoproject.com/en/2.2/)
- [Pipenv Documentation](https://pipenv.readthedocs.io/en/latest/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)


