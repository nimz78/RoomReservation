# Room Reservation App

A room reservation REST api implemented in Django.

## Setup

First clone the repository:
    
    $ git clone https://github.com/nimz78/RoomReservation.git
    $ cd RoomReservation

Second create virtualenv inside the project directory:

    $ python3 -m venv .venv


Third activate the virtualenv:

    $ source .venv/bin/activate

Install packages from requirements.txt file:

    $ pip install -r requirements.txt

Making migrations:

    $ python manage.py makemigrations

Then simply apply the migrations:

    $ python manage.py migrate

You can now run the development server:

    $ python manage.py runserver

## Usage

To create room (Room post method):

    http://127.0.0.1:8000/api/rooms/
Body:

    {
    "title": "Room name",
    "description": "Write description about Room",
    "adults": 3,
    "price_per_night": 300000,
    "breakfast_included": false
    }


To read all rooms (Room get method):

    http://127.0.0.1:8000/api/rooms


To read specific room by ID (Room get method):

    http://127.0.0.1:8000/api/rooms/1


To update specific room by ID (Room put method):

    http://127.0.0.1:8000/api/rooms/1
Body:

    {
    "title": "Update title",
    "description": "Update description's Room",
    "adults": 3,
    "price_per_night": 300000,
    "breakfast_included": false
    }

To delete specific room by ID (Room delete method):

    http://127.0.0.1:8000/api/rooms/1


To reserve a room (Reservation Post method):

    http://127.0.0.1:8000/api/rooms/1/reservations
Body:

    {
    "from_date": "2023-02-05",
    "to_date": "2023-02-06",
    "customer_name": "Costomer name"
    }


To read reserved room (Reservation get method):

    http://127.0.0.1:8000/api/rooms/3/reservations


To Browse a list of reservations(HTML):

    http://127.0.0.1:8000/reports/
