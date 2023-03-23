import random
from rest_framework import serializers
from .models import Room, Reservation


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "id",
            "title",
            "description",
            "adults",
            "price_per_night",
            "breakfast_included",
        )


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = (
            "id",
            "from_date",
            "to_date",
            "total_price",
            "customer_name",
            "voucher_code",
            "room"
        )