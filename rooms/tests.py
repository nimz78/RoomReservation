from django.test import RequestFactory, TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rooms.models import Room
from rooms.serializers import RoomSerializer, ReservationSerializer
from rooms.models import Reservation
from datetime import datetime, timedelta


class RoomListApiViewAPITestCase(APITestCase):
    def setUp(self):
        self.room_data = {
            "title": "Example Room",
            "description": "This is an example room",
            "adults": 2,
            "price_per_night": 100,
            "breakfast_included": True
        }
        self.url = reverse('room-list', kwargs={})

    def test_get_list(self):
        response = self.client.get(self.url)
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_room(self):
        response = self.client.post(self.url, self.room_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), 1)
        self.assertEqual(Room.objects.get().title, self.room_data['title'])

    def test_create_room_with_invalid_data(self):
        invalid_room_data = {
            "title": "Example Room",
            "description": "This is an example room",
            "adults": "invalid data",
            "price_per_night": 100,
            "breakfast_included": True
        }
        response = self.client.post(self.url, invalid_room_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Room.objects.count(), 0)


class RoomDetailApiViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.room = Room.objects.create(
            title='Test Room',
            description='This is a test room',
            adults=2,
            price_per_night=100,
            breakfast_included=True
        )
        self.valid_payload = {
            "title": "Update tiiitle",
            "description": "Update description's Room",
            "adults": 3,
            "price_per_night": 300000,
            "breakfast_included": False
        }
        self.invalid_payload = {
            'title': '',
            'description': 'This is an invalid test room',
            'adults': -1,
            'price_per_night': 0,
            'breakfast_included': "invlaid detail"
        }
        self.reserve_url = reverse('room-detail', args=[self.room.id])

    def test_get_valid_room(self):
        response = self.client.get(self.reserve_url)
        serializer = RoomSerializer(instance=self.room)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_room(self):
        response = self.client.get(reverse('room-detail', args=[99999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_valid_room(self):
        response = self.client.put(self.reserve_url, self.valid_payload)
        self.room.refresh_from_db()
        serializer = RoomSerializer(instance=self.room)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_room_with_invalid_body(self):
        response = self.client.put(self.reserve_url, self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_valid_room(self):
        response = self.client.delete(self.reserve_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Room.objects.filter(id=self.room.id).exists())

    def test_delete_invalid_room(self):
        response = self.client.delete(reverse('room-detail', args=[99999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ReservationApiViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.room = Room.objects.create(
            title="Deluxe Room",
            description="A spacious room with a king-sized bed and a balcony.",
            adults=2,
            price_per_night=200,
            breakfast_included=True
        )
        self.reservation = Reservation.objects.create(
            from_date=datetime.now(),
            to_date=datetime.now() + timedelta(days=2),
            total_price=400,
            customer_name="Test User",
            voucher_code="123456",
            room=self.room
        )
        self.valid_payload = {
            'from_date': (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'),
            'to_date': (datetime.now().date() + timedelta(days=15)).strftime('%Y-%m-%d'),
            'customer_name': 'Test user'
        }
        self.invalid_payload = {
            'from_date': datetime.now().strftime('%Y-%m-%d'),
            'to_date': (datetime.now().date() + timedelta(days=2)).strftime('%Y-%m-%d'),
            'customer_name': ''
        }
        self.overlap_payload = {
            'from_date': datetime.now().strftime('%Y-%m-%d'),
            'to_date': (datetime.now().date() + timedelta(days=1)).strftime('%Y-%m-%d'),
            'customer_name': 'Test user'
        }
        self.valid_payload_put = {
            'from_date': (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'),
            'to_date': (datetime.now().date() + timedelta(days=15)).strftime('%Y-%m-%d'),
            'customer_name': 'Test user',
            "total_price": 300000,
            "voucher_code": 23456,
            "room": self.room.id
        }
        self.invalid_payload_put = {
            'from_date': datetime.now().strftime('%Y-%m-%d'),
            'to_date': (datetime.now().date() + timedelta(days=2)).strftime('%Y-%m-%d'),
            'customer_name': '',
            "total_price": 300000,
            "voucher_code": 23456,
            "room": self.room.id
        }
        self.overlap_payload_put = {
            'from_date': datetime.now().strftime('%Y-%m-%d'),
            'to_date': (datetime.now().date() + timedelta(days=1)).strftime('%Y-%m-%d'),
            'customer_name': 'Test user',
            "total_price": 300000,
            "voucher_code": 23456,
            "room": self.room.id
        }
        self.url = reverse('reservation', kwargs={'room_id': self.room.id})
        self.url_put = reverse('reservation-detail', kwargs={'room_id': self.room.id, 'reservation_id': self.reservation.id})

    def test_get_valid_reservation(self):
        response = self.client.get(self.url)
        reservations = Reservation.objects.filter(room_id=self.room.id)
        serializer = ReservationSerializer(reservations, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_reservation(self):
        url = reverse('reservation', kwargs={'room_id': 505})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_valid_reservation(self):
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_with_has_overlap(self):
        response = self.client.post(self.url, data=self.overlap_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_invalid_reservation(self):
        response = self.client.post(self.url, data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_valid_reservation(self):
        response = self.client.put(self.url_put, data=self.valid_payload_put)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_invalid_reservation(self):
        response = self.client.put(self.url_put, data=self.invalid_payload_put)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_with_has_overlap(self):
        response = self.client.put(self.url_put, data=self.overlap_payload_put)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_reservation(self):
        response = self.client.delete(self.url_put)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Reservation.objects.filter(id=self.reservation.id).exists())

    def test_delete_invalid_reservation(self):
        url_invalid = reverse('reservation-detail', kwargs={'room_id': self.room.id, 'reservation_id': 1000})
        response = self.client.delete(url_invalid)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Reservation.objects.filter(id=self.reservation.id).exists())