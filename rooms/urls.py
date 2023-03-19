from django.urls import path

from .views import ReservationApiView, RoomDetailApiView, RoomListApiView

urlpatterns = [
    path('', RoomListApiView.as_view()),
    path('<int:room_id>', RoomDetailApiView.as_view()),
    path('<int:room_id>/reservations', ReservationApiView.as_view()),
]
