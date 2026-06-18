from django.db import models
from django.contrib import admin
from facilities.models import Room
from accounts.models import Account
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


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

    @admin.display(description=_("Duration of meeting"))
    def meeting_duration(self) -> int:
        """Returns meeting duration in minutes"""
        return (self.end_date - self.start_date).total_seconds() // 60

    def clean(self):
        super().clean()

        if not (self.start_date and self.end_date and self.room_id):
            raise ValidationError(_("The key fields are missing!"))

        time_now = timezone.now()

        if self.start_date < time_now or self.end_date < time_now:
            raise ValidationError(
                _("Start date and start date should not be in the past!")
            )

        if self.start_date >= self.end_date:
            raise ValidationError(_("End date should be later than start date"))

        overlapping_reservations = Reservation.objects.filter(
            room_id=self.room_id,
            start_date__lt=self.end_date,  # There is reservation that starts before end_date
            end_date__gt=self.start_date,  # There is reservation that ends after start date
        ).exclude(pk=self.pk)  # excludes current one

        if overlapping_reservations.exists():
            raise ValidationError(_("This room is already reserved for this time!"))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.start_date} - {self.end_date} : {self.room}, {self.account}"
