import datetime

import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone

from .models import Reservation


@pytest.mark.reservations
@pytest.mark.django_db
class TestReservation:
    """tests reservation model"""

    def test_creation(self, def_reservation, def_room, user_st):
        assert def_reservation.room == def_room
        assert def_reservation.account == user_st

        expected_start = timezone.now() + datetime.timedelta(days=5)
        expected_end = timezone.now() + datetime.timedelta(days=5, hours=2, minutes=30)

        assert abs((def_reservation.start_date - expected_start).total_seconds()) < 2
        assert abs((def_reservation.end_date - expected_end).total_seconds()) < 2

        expected_duration = datetime.timedelta(hours=2, minutes=30)
        tested_duration = def_reservation.end_date - def_reservation.start_date

        assert abs(tested_duration - expected_duration) < datetime.timedelta(seconds=2)

        assert (timezone.now() - def_reservation.creation_date).total_seconds() < 2

    def test_uniqueness_db(self, def_reservation, def_room, user_st):
        """
        tests if uniqueness is enforced (direct, db approach)
        method "save" is overwritten and should result in ValidationError being raised
        """

        with pytest.raises(ValidationError):
            Reservation.objects.create(
                room=def_room,
                account=user_st,
                # year, month, day, hour, minute
                start_date=def_reservation.start_date,
                end_date=def_reservation.end_date,
            )

    def test_uniqueness_validation(self, def_reservation, def_room, user_st):
        """tests if uniqueness is enforced (run with checkers)"""

        with pytest.raises(ValidationError):
            dupe = Reservation(
                room=def_room,
                account=user_st,
                # year, month, day, hour, minute
                start_date=def_reservation.start_date,
                end_date=def_reservation.end_date,
            )

            dupe.full_clean()

    def test_duration_calculation(self, def_reservation):
        """tests if calculating reservation duration is correct"""

        assert def_reservation.meeting_duration() == 150


@pytest.mark.reservationViews
@pytest.mark.django_db
class TestReservationViews:
    def test_reservation_all(self, client, def_three_reservs):
        """tests if all reservations are returned"""

        url = reverse("api_reservations")

        response = client.get(url)
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 3

    def test_reservation_room(self, client, def_room, def_three_reservs):
        """tests if all reservations are returned"""

        url = reverse("api_reservations")

        response_without_acc = client.get(url, data={"room_id": def_room.id})
        assert response_without_acc.status_code == 200

        data = response_without_acc.json()
        assert len(data) == 2

    def test_reservation_room_acc(
        self, client, def_reservation, def_three_reservs, def_room, user_st, user_ad
    ):
        """tests more advanced API compatibility"""

        # first we check if for account that has data
        url = reverse("api_reservations")

        response_correct_acc = client.get(
            url, data={"room_id": def_room.id, "account_id": user_st.id}
        )

        assert response_correct_acc.status_code == 200
        data_recived = response_correct_acc.json()

        assert data_recived[0]["title"] == f"{def_reservation.account!s}"
        assert data_recived[0]["start"] == def_reservation.start_date.isoformat()
        assert data_recived[0]["end"] == def_reservation.end_date.isoformat()

        # next we check account that has not made any reservations
        response_incorrect_acc = client.get(
            url, data={"room_id": def_room.id, "account_id": user_ad.id}
        )
        assert response_incorrect_acc.status_code == 200

        data = response_incorrect_acc.json()
        assert not data


@pytest.mark.healthchecks
class TestHealthchecks:
    def test_liveness_probe(self, client):
        """Tests if the liveness probe returns 200 OK without DB connection"""

        url = reverse("http_healthcheck")

        response = client.get(url)
        assert response.status_code == 200
        assert response.content == b""

    @pytest.mark.django_db
    def test_readiness_probe_success(self, client):
        """Tests if the readiness probe returns 200 OK when DB is connected"""

        url = reverse("db_healthcheck")

        response = client.get(url)
        assert response.status_code == 200
        assert response.content == b"Database ready"
