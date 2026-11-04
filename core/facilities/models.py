from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Building(models.Model):
    id = models.AutoField(
        primary_key=True,
        verbose_name=_("Building's id"),
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_("Building's name"),
    )

    city = models.CharField(
        max_length=255,
        verbose_name=_("Building's location"),
    )

    street = models.CharField(
        max_length=255,
        verbose_name=_("Building's street name"),
    )

    number = models.CharField(
        max_length=64,
        verbose_name=_("Building's number"),
    )

    # I live in Poland, so postal codes are like xx-xxx
    postal_code = models.CharField(
        max_length=6,
        verbose_name=_("Building's location postal code"),
        validators=[
            RegexValidator(
                regex=r"^\d{2}-\d{3}$",
                message=_("Postal code in Poland takes the form of: XX-XXX"),
            )
        ],
    )

    class Meta:
        verbose_name = _("building")
        verbose_name_plural = _("buildings")
        abstract = False

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "city",
                    "street",
                    "number",
                    "postal_code",
                ],
                name="unique_buildings",
            )
        ]

    def __str__(self):
        return f"{self.name}, {self.city}/{self.postal_code}"

    def __repr__(self):
        return f"{self.id} - {self.name} | {self.city}/{self.postal_code}"


class Room(models.Model):
    class RoomType(models.TextChoices):
        CLASSROOM = "CLASS", _("Classroom")
        FULLCONF = "FCONF", _("Full Conference Room")
        MULTICONF = "MCONF", _("Mulitpurpose Conference Room")

    class RoomSize(models.TextChoices):
        SMALL = "S", _("Small (up to 10 people)")
        MEDIUM = "M", _("Medium (up to 35 people)")
        LARGE = "L", _("Large (up to 65 people)")
        XLARGE = "XL", _("Extra Large (up to 100 people)")

    class RoomPrice(models.IntegerChoices):
        LOW = 10, _("Low cost")
        MED = 25, _("Medium cost")
        HIGH = 50, _("High cost")

    id = models.AutoField(
        primary_key=True,
        verbose_name=_("Room's id"),
    )

    building = models.ForeignKey(
        to=Building,
        on_delete=models.CASCADE,
        verbose_name=_("The building the room belongs to"),
    )

    section = models.CharField(
        max_length=64,
        verbose_name=_("Section of the building where the room is located"),
    )

    number = models.CharField(
        max_length=32,
        verbose_name=_("Room's number"),
    )

    type = models.CharField(
        verbose_name=_("Room's type"),
        max_length=255,
        choices=RoomType,
        default=RoomType.MULTICONF,
    )

    size = models.CharField(
        verbose_name=_("Room's size"),
        max_length=255,
        choices=RoomSize,
        default=RoomSize.MEDIUM,
    )

    price = models.IntegerField(
        verbose_name=_("Room's price per 1m2"),
        choices=RoomPrice,
        default=RoomPrice.MED,
    )

    class Meta:
        verbose_name = _("room")
        verbose_name_plural = _("rooms")
        abstract = False

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "building",
                    "section",
                    "number",
                ],
                name="unique_rooms",
            )
        ]

    @property
    def city(self):
        return self.building.city

    def __str__(self):
        return f"{self.section}/{self.number}/{self.building}"

    def __repr__(self):
        return f"{self.id} - {self.section}/{self.number}"
