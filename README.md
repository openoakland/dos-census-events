# Census events and resources

Find census events and resources near you.


## "Goals"

- Events and resources
- Partners can enter event information through forms
- Events are published to google calendar
- Export events via CSV
- Integrate with SwORD via CSV export


## Usage

### Create calendar events

[Create an event](http://localhost:8000/admin/census/event/add/).


## Development


### Prerequisites

- Python 3
- virtualenv

We assume you are installing to a python virtualenv.


### Setup

Install python dependencies.

    $ pip install -r requirements.txt

Initialize the database.

    $ python manage.py migrate

Create an admin user by following the prompts.

    $ python manage.py createsuperuser


### Working with database migrations

Anytime you make a change to the models, you should try to run makemigrations to
generate a database migration.

    $ python manage.py makemigrations census
