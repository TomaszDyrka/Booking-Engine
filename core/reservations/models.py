from django.db import models
from ..facilities.models import Room, Building
from ..accounts.models import Account
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Reservation(models.Model):
    id = models.AutoField(
        primary_key=True,
        verbose_name=_("Reservation's id"),
    )

    room = models.ForeignKey(
        to=Room, 
        on_delete=models.PROTECT,
        verbose_name=_("The reserved room"),
    )

    account = models.ForeignKey(
        to=Account,
        on_delete=models.PROTECT,
        verbose_name=_("The account reserving room"),
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Creation date"),
    )

    start_date = models.DateTimeField(
        verbose_name=_("Starting time"),
    )

    end_date = models.DateTimeField(
        verbose_name=_("Ending time"),
    )

    @admin.display(
        description=_("Duration of meeting"),
        )
    @property
    def meeting_duration(self) -> int:
        """Returns meeting duration in minutes"""
        return (self.end_date - self.start_date).total_seconds() // 60

    def __str__(self):
        return f"{self.end_date} - {self.start_date} : {self.room}, {self.account}"