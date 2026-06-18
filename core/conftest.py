import pytest
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from facilities.models import Building, Room
from reservations.models import Reservation


@pytest.fixture
def user_st(db):
    """Test Standard account"""

    Account = get_user_model()
    acc = Account.objects.create_user(
        email="test@user.com",
        first_name="John",
        last_name="Doe",
        password="foo",
        pesel="12312312311",
    )

    return acc


@pytest.fixture
def user_ad(db):
    """Test Administrator account"""

    Account = get_user_model()
    acc = Account.objects.create_superuser(
        email="test@admin.com",
        first_name="John",
        last_name="Doe",
        password="foo",
        pesel="12312312312",
    )

    return acc


@pytest.fixture
def user_md(db):
    """Test Moderator account"""

    Account = get_user_model()
    acc = Account.objects.create_moderator(
        email="test@mod.com",
        first_name="John",
        last_name="Doe",
        password="foo",
        pesel="12312312313",
    )

    return acc


@pytest.fixture
def def_building(db):
    return Building.objects.create(
        name="Main Building",
        city="Cracow",
        street="Wroclawska",
        number="10",
        postal_code="23-412",
    )


@pytest.fixture
def def_room(db, def_building):
    return Room.objects.create(
        building=def_building,
        section="A",
        number="13",
        type=Room.RoomType.CLASSROOM,
        size=Room.RoomSize.LARGE,
        price=Room.RoomPrice.HIGH,
    )


@pytest.fixture
def def_room_2(db, def_building):
    return Room.objects.create(
        building=def_building,
        section="B",
        number="20",
        type=Room.RoomType.CLASSROOM,
        size=Room.RoomSize.LARGE,
        price=Room.RoomPrice.HIGH,
    )


@pytest.fixture
def def_reservation(db, def_room, user_st):
    return Reservation.objects.create(
        room=def_room,
        account=user_st,
        # year, month, day, hour, minute
        start_date=timezone.now() + timedelta(days=5),
        end_date=timezone.now() + timedelta(days=5, hours=2, minutes=30),
    )


@pytest.fixture
def def_reservation_2(db, def_room, user_md):
    return Reservation.objects.create(
        room=def_room,
        account=user_md,
        # year, month, day, hour, minute
        start_date=timezone.now() + timedelta(days=6),
        end_date=timezone.now() + timedelta(days=6, hours=2, minutes=30),
    )


@pytest.fixture
def def_reservation_3(db, def_room_2, user_md):
    return Reservation.objects.create(
        room=def_room_2,
        account=user_md,
        # year, month, day, hour, minute
        start_date=timezone.now() + timedelta(days=6),
        end_date=timezone.now() + timedelta(days=6, hours=2, minutes=30),
    )


@pytest.fixture
def def_three_reservs(def_reservation, def_reservation_2, def_reservation_3):
    pass
