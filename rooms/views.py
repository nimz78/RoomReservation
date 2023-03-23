import datetime
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Reservation, Room
from .serializers import ReservationSerializer, RoomSerializer
from .utils import date_util
import random


class RoomListApiView(APIView):
    def get(self, request, *args, **kwargs):
        rooms = Room.objects.filter()
        serializer = RoomSerializer(rooms, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = RoomSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoomDetailApiView(APIView):
    def get_object(self, room_id):
        try:
            return Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return None

    def get(self, request, room_id, *args, **kwargs):
        room_instance = self.get_object(room_id)

        if not room_instance:
            return Response(
                {"message": "Object with room id does not exists"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = RoomSerializer(room_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, room_id, *args, **kwargs):
        room_instance = self.get_object(room_id)

        if not room_instance:
            return Response(
                {"message": "Object with room id does not exists"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = RoomSerializer(
            instance=room_instance, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, room_id, *args, **kwargs):
        room_instance = self.get_object(room_id)

        if not room_instance:
            return Response(
                {"message": "Object with room id does not exists"},
                status=status.HTTP_404_NOT_FOUND
            )

        room_instance.delete()

        return Response(
            {"message": "Reservation deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


class ReservationApiView(APIView):
    def get_object(self, room_id, reservation_id=None):
        if reservation_id is not None:
            try:
                return Reservation.objects.get(room_id=room_id, id=reservation_id)
            except Reservation.DoesNotExist:
                return None
        try:
            return Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return None

    def get(self, request, room_id, *args, **kwargs):
        room_instance = self.get_object(room_id)

        if not room_instance:
            return Response(
                {"message": "Object with room id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        reservations = Reservation.objects.filter(room_id=room_instance.id)
        serializer = ReservationSerializer(reservations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, room_id, *args, **kwargs):

        room_instance = self.get_object(room_id)

        if not room_instance:
            return Response(
                {"message": "Object with room id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        if datetime.datetime.strptime(request.data['from_date'], "%Y-%m-%d").date() < datetime.date.today():
            return Response(
                {"message": "Reservation cannot be made for an expired date"},
                status=status.HTTP_400_BAD_REQUEST
            )

        last_room_reservations = Reservation.objects.filter(
            room_id=room_instance.id
        )

        has_overlap = False
        for reservation in last_room_reservations:
            if date_util.is_overlapped(
                [
                    (
                        date_util.parse_date(request.data['from_date']),
                        date_util.parse_date(request.data['to_date']),
                    ),
                    ((reservation.from_date, reservation.to_date)),
                ]
            ):
                has_overlap = True

        if has_overlap:
            return Response(
                {"message": "Selected time range is booked, try another time range!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        nights_stay_delta = date_util.parse_date(
            request.data['to_date']
        ) - date_util.parse_date(request.data['from_date'])

        reservation_data = {
            "from_date": request.data['from_date'],
            "to_date": request.data['to_date'],
            "total_price": nights_stay_delta.days * room_instance.price_per_night,
            "customer_name": request.data['customer_name'],
            "voucher_code": str(random.randint(100000, 999999)),
            "room": room_instance.id,
        }

        serializer = ReservationSerializer(data=reservation_data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, room_id, reservation_id, *args, **kwargs):
        room_instance = self.get_object(room_id)

        if not room_instance:
            return Response(
                {"message": "Object with room id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        reservation_instance = self.get_object(room_id, reservation_id)

        if not reservation_instance:
            return Response(
                {"message": "Object with reservation id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ReservationSerializer(
            reservation_instance, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if datetime.datetime.strptime(request.data['from_date'], "%Y-%m-%d").date() < datetime.date.today():
            return Response(
                {"message": "Reservation cannot be made for an expired date"},
                status=status.HTTP_400_BAD_REQUEST
            )

        last_room_reservations = Reservation.objects.filter(
            room_id=room_instance.id).exclude(id=reservation_id)
        has_overlap = False
        for reservation in last_room_reservations:
            if date_util.is_overlapped([(date_util.parse_date(request.data['from_date']), date_util.parse_date(request.data['to_date'])), ((
                    reservation.from_date, reservation.to_date))]):
                has_overlap = True

        if has_overlap:
            return Response(
                {"message": "Selected time range is booked, try another time range!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        nights_stay_delta = date_util.parse_date(
            request.data['to_date']) - date_util.parse_date(request.data['from_date'])

        reservation_data = {
            "from_date": request.data['from_date'],
            "to_date": request.data['to_date'],
            "total_price": nights_stay_delta.days * room_instance.price_per_night,
            "customer_name": request.data['customer_name'],
            "voucher_code": str(random.randint(100000, 999999)),
            "room": room_instance.id
        }

        serializer = ReservationSerializer(
            reservation_instance, data=reservation_data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, room_id, reservation_id, *args, **kwargs):
        reservation_instance = self.get_object(room_id, reservation_id)

        if not reservation_instance:
            return Response(
                {"message": "Object with reservation id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        reservation_instance.delete()

        return Response(
            {"message": "Reservation deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
