from django.urls import path

from .views import geeks_view

urlpatterns = [
    path('', geeks_view),
]
