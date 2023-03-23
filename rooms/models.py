from django.db import models


class Room(models.Model):
    title = models.CharField(max_length=30, blank=False)
    description = models.CharField(max_length=100, blank=False)
    adults = models.IntegerField(blank=False)
    price_per_night = models.IntegerField(blank=False)
    breakfast_included = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Reservation(models.Model):
    from_date = models.DateField(blank=False)
    to_date = models.DateField(blank=False)
    total_price = models.IntegerField(blank=False)
    customer_name = models.CharField(max_length=30, blank=False)
    voucher_code = models.CharField(blank=False, max_length=30, unique=True)

    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer_name
