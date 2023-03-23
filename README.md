# Room Reservation App

A room reservation REST api implemented in Django.

## SUMMARY

The reservation management project has 2 applications

1-Rooms: 
    you can create a room which has 5 fields; title is a short descrption about room (like a name), description is a compelete description about room, adualts means acceptable number of people, price per night is coust of renting room per night, breakfast included is clear that is boolian.
    In this application we have another table witch has 6 fields that save reservation information ; frome date means the start time of reservation, to date means the end time of reservation, customer name is clear that is name of person who reserve the room, voucher code is a code that generate automaticlly and it is like a unique id of the reservation which is human readable, room which is foreignkey of this table.

2-reports:
    This application shows all rooms and costumer and reservation information so it can browse a list of reservations as a HTML table in a browser.

## SETUP

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

## USAGE

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

To update and edite spesific reservation (Reservation Put method):

    http://127.0.0.1:8000/api/rooms/1/reservations/1
Body:

    {
    "from_date": "2023-07-20",
    "to_date": "2023-07-21",
    "customer_name": "Edit Costumer name",
    "total_price": 300000,
    "voucher_code": 23456,
    "room": 4
    }

To read reservations of a room (Reservation get method):

    http://127.0.0.1:8000/api/rooms/3/reservations

To delete spesific reservation of a room (Reservation Delete method):

    http://127.0.0.1:8000/api/rooms/1/reservations/1


To Browse a list of reservations(HTML):

    http://127.0.0.1:8000/reports/


## UNITTEST USAGE
 
To run unittest python please write this command in your terminal:

python manage.py test rooms  