from django.urls import path
from .views import (
    ReservationsEventsAPIView,
    RoomDetailView,
    RoomListView,
    http_healthcheck,
    db_healthcheck,
)


urlpatterns = [
    # For getting reservations
    path(
        "api/reservations/",
        ReservationsEventsAPIView.as_view(),
        name="api_reservations",
    ),
    # Calendar full suite
    path("room/<int:pk>/", RoomDetailView.as_view(), name="room_detail"),
    # Room view/Main page
    path("", RoomListView.as_view(), name="home"),
    path("live/", http_healthcheck, name="http_healthcheck"),
    path("ready/", db_healthcheck, name="db_healthcheck"),
]
