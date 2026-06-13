from django.urls import path
from .views import ReservationsEventsAPIView, RoomDetailView, RoomListView


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
]
