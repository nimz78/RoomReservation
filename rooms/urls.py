from django.urls import path

from .views import ReservationApiView, RoomDetailApiView, RoomListApiView

urlpatterns = [
    path('', RoomListApiView.as_view(), name='room-list'),
    path('<int:room_id>', RoomDetailApiView.as_view(), name='room-detail'),
    path('<int:room_id>/reservations', ReservationApiView.as_view(), name='reservation'),
    path('<int:room_id>/reservations/<int:reservation_id>', ReservationApiView.as_view(), name='reservation-detail'),
]
