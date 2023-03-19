from django.shortcuts import render
from rooms.models import Reservation


def geeks_view(request):
    reservations = Reservation.objects.filter()

    return render(request, "index.html", {"reservations": reservations})
