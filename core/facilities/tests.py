import pytest
from .models import Room, Building
from django.db import IntegrityError
from django.core.exceptions import ValidationError


@pytest.fixture
def def_building():
    return Building.objects.create(
        name="Main Building",
        city="Cracow",
        street="Wroclawska",
        number="10",
        postal_code="23-412",
    )


@pytest.fixture
def def_room(def_building):
    return Room.objects.create(
        building=def_building,
        section="A",
        number="13",
        type=Room.RoomType.CLASSROOM,
        size=Room.RoomSize.LARGE,
        price=Room.RoomPrice.HIGH,
    )


@pytest.mark.facilities
@pytest.mark.django_db
class TestModels:
    """Test models"""

    def test_create_room(self, def_room, def_building):
        """tests room creation"""

        # tests correctness
        assert def_room.building == def_building
        assert def_room.section == "A"
        assert def_room.number == "13"
        assert def_room.type == Room.RoomType.CLASSROOM
        assert def_room.size == Room.RoomSize.LARGE
        assert def_room.price == Room.RoomPrice.HIGH

    def test_uniqueness_rooms_id(self, def_room, def_building):
        """
        tests if rooms have properly implemented unique necesseary set of records:
        - building
        - section
        - number
        """

        # tests creation of different, other room
        new_room = Room.objects.create(
            building=def_building,
            section="A",
            number="14",
            type=Room.RoomType.CLASSROOM,
            size=Room.RoomSize.LARGE,
            price=Room.RoomPrice.HIGH,
        )

        # tests exclusivity of id
        assert def_room.id != new_room.id

    def test_uniqueness_rooms_db(self, def_room, def_building):
        """tests uniquness of rooms (direct, db approach)"""

        with pytest.raises(IntegrityError):
            Room.objects.create(
                building=def_building,
                section="A",
                number="13",
                type=Room.RoomType.CLASSROOM,
                size=Room.RoomSize.LARGE,
                price=Room.RoomPrice.HIGH,
            )

    def test_uniqueness_rooms_validation(self, def_room, def_building):
        """tests uniqueness of rooms (run with checkers)"""
        with pytest.raises(ValidationError):
            dupe = Room(
                building=def_building,
                section="A",
                number="13",
                type=Room.RoomType.CLASSROOM,
                size=Room.RoomSize.LARGE,
                price=Room.RoomPrice.HIGH,
            )

            dupe.full_clean()

    def test_create_building(self, def_building):
        """tests building creation"""

        assert def_building.name == "Main Building"
        assert def_building.city == "Cracow"
        assert def_building.street == "Wroclawska"
        assert def_building.number == "10"
        assert def_building.postal_code == "23-412"

    def test_uniqueness_buildings_id(self, def_building):
        """
        tests if buildings have properly implemented unique necesseary set of records:
        - location
        - street
        - number
        - postal_code
        """

        # tests creation of different, other room
        new_building = Building.objects.create(
            name="Workshop",
            city="Warsaw",
            street="al. Jerozolimskie",
            number="11",
            postal_code="12-345",
        )

        # test exclusivity of id
        assert def_building.id != new_building.id

    def test_uniqueness_buildings_db(self, def_building):
        """tests uniqueness of buildings, direct approach"""

        with pytest.raises(IntegrityError):
            Building.objects.create(
                name="Main Building",
                city="Cracow",
                street="Wroclawska",
                number="10",
                postal_code="23-412",
            )

    def test_uniqueness_buildings_validation(self, def_building):
        """tests uniqueness of buildings, run with checkers"""

        with pytest.raises(ValidationError):
            dupe = Building(
                name="Main Building",
                city="Cracow",
                street="Wroclawska",
                number="10",
                postal_code="23-412",
            )

            dupe.full_clean()
