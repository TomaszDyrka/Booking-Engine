import logging

from django.contrib import messages
from django.db import OperationalError, connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView, ListView
from facilities.models import Room

from .forms import ReservationForm
from .models import Reservation

logger = logging.getLogger(__name__)


def http_healthcheck(*args, **kwargs):
    """Healthcheck for liveliness probe"""
    logger.info("Liveliness check")
    return HttpResponse(status=200)


def db_healthcheck(*args, **kwargs):
    """Healthcheck for readiness probe"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            logger.info("Readiness check")
            return HttpResponse("Database ready", status=200)
    except OperationalError:
        logger.error("Readiness probe failed - database is down!")
        return HttpResponse("Database unavailable", status=503)


class RoomDetailView(DetailView):
    """
    view for handling forms (creating reservations)

    by default, bare DetailViews doesn't get along with
    doing anything beside showing an entry from a table,
    so I "ramped" it slightly
    """

    model = Room
    template_name = "reservations/room_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "form" not in context:
            context["form"] = ReservationForm(instance=Reservation(room=self.object))

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            messages.error(request, "Only logged in users can book a room!.")
            return self.render_to_response(self.get_context_data(), status=400)

        form = ReservationForm(
            request.POST, instance=Reservation(room=self.object, account=request.user)
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Reservation has been added!")
            return redirect("room_detail", pk=self.object.pk)
        else:
            # I have written some error explainations in model class, so why not use them here
            if form.non_field_errors():
                for error in form.non_field_errors():
                    messages.error(request, error)

            else:
                messages.error(
                    request,
                    "Something went wrong! Be sure you have put everything correctly.",
                )

            return self.render_to_response(self.get_context_data(form=form), status=400)

        return self.render_to_response(self.get_context_data(form=form))


class RoomListView(ListView):
    model = Room
    template_name = "reservations/home.html"
    context_object_name = "rooms"


class ReservationsEventsAPIView(View):
    """
    view for extracting info from database
    """

    def get(self, request, *args, **kwargs):
        room_id = request.GET.get("room_id")
        account_id = request.GET.get("account_id")

        reservations = Reservation.objects.all()

        if room_id:
            reservations = reservations.filter(room_id=room_id)
        if account_id:
            reservations = reservations.filter(account_id=account_id)

        events = []
        for reserv in reservations:
            title = f"{reserv.account!s}"

            events.append(
                {
                    "title": title,
                    "start": reserv.start_date.isoformat(),
                    "end": reserv.end_date.isoformat(),
                }
            )

        return JsonResponse(events, safe=False)
