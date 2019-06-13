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


#### Install the requirements, initialize database and create a super user:

Install python dependencies.

    $ pipenv install -r requirements.txt

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