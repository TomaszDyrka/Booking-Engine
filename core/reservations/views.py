from django.http import JsonResponse
from django.views.generic import CreateView, DetailView
from django.views import View
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Reservation
from facilities.models import Room
from .forms import ReservationForm


class RoomDetailView(DetailView):
    model = Room
    template_name = "reservations/room_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form"] = ReservationForm()
        return context


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "reservations/reservation_form.html"

    def form_valid(self, form):
        form.instance.account = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = Reservation(room_id=self.kwargs['room_id'])
        
        return kwargs

    def get_success_url(self):
        return reverse("room_detail", kwargs={"pk": self.kwargs["room_id"]})


class ReservationsEventsAPIView(View):
    def get(self, request, *args, **kwargs):
        reservations = Reservation.objects.filter(room_id=kwargs["room_id"])
        events = []

        for reserv in reservations:
            title = f"{str(reserv.room)} {str(reserv.account)}"

            events.append(
                {
                    "title": title,
                    "start": reserv.start_date.isoformat(),
                    "end": reserv.end_date.isoformat(),
                }
            )

        return JsonResponse(events, safe=False)
