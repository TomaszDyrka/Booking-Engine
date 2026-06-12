from django.urls import path
from .views import ReservationCreateView, ReservationsEventsAPIView, RoomDetailView


urlpatterns = [
    # Path to creation form
    path(
        "nowa/<int:room_id>/", ReservationCreateView.as_view(), name="reservation_create"
    ),

    # For getting reservations
    path(
        "api/reservations/<int:room_id>/",
        ReservationsEventsAPIView.as_view(),
        name="api_reservations",
    ),
    
    # New 'calendar'
    path("room/<int:pk>/", RoomDetailView.as_view(), name="room_detail"),
]
