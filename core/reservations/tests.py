import pytest
import datetime
from .models import Reservation
from django.db import IntegrityError
from django.core.exceptions import ValidationError

# Create your tests here.
pytset_plugins = [
    "accounts.tests",
    "facilities.tests",
]

@pytest.fixture
def def_reservation(def_room, user_st):
    return Reservation.objects.create(
        room=def_room,
        account=user_st,
        # year, month, day, hour, minute
        start_date=datetime.datetime(2050, 1, 20, 10, 0),
        end_date=datetime.datetime(2050, 1, 20, 12, 30),
        )

@pytest.mark.reservations
@pytest.mark.django_db
class TestReservation:
    """tests reservation model"""

    def test_creation(self, def_reservation, def_room, user_st):
        """tests reservation creation"""

        assert def_reservation.room == def_room
        assert def_reservation.account == user_st
        assert def_reservation.start_date == datetime.datetime(2050, 1, 20, 10, 0)
        assert def_reservation.end_date == datetime.datetime(2050, 1, 20, 12, 30)

        assert (datetime.now() - def_reservation.booking_date).seconds < 1

    def test_uniqueness_db(self, def_reservation, def_room, user_st):
        """tests if uniqueness is enforced (direct, db approach)"""

        with pytest.raises(IntegrityError):
            Reservation.objects.create(
                room=def_room,
                account=user_st,
                # year, month, day, hour, minute
                start_date=datetime.datetime(2050, 1, 20, 10, 0),
                end_date=datetime.datetime(2050, 1, 20, 12, 30),
                )

    def test_uniqueness_validation(self, def_reservation, def_room, user_st):
        """tests if uniqueness is enforced (run with checkers)"""
        with pytest.raises(ValidationError):
            dupe = Reservation(
                room=def_room,
                account=user_st,
                # year, month, day, hour, minute
                start_date=datetime.datetime(2050, 1, 20, 10, 0),
                end_date=datetime.datetime(2050, 1, 20, 12, 30),
                )

            dupe.full_clean()

    def test_duration_calculation(self, def_reservation):
        """tests if calculating reservation duration is correct""" 
        assert def_reservation.meeting_duration == 150
    



