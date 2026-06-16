from .forms import CustomAccountCreationForm
from reservations.models import Reservation
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.shortcuts import redirect


class RegisterView(CreateView):
    """quick view that takes care of registrating users"""

    form_class = CustomAccountCreationForm
    template_name = "registrations/register.html"

    success_url = reverse_lazy("login")


class ProfileListView(ListView):
    """
    view that handles profile based actions
    (listing accounts reservations and deleting them)
    """

    model = Reservation
    template_name = "accounts/profile.html"

    def get_queryset(self):
        return Reservation.objects.filter(account=self.request.user)

    def post(self, request, *args, **kwargs):
        if reservation_id := request.POST.get("reservation_id"):
            Reservation.objects.filter(
                id=reservation_id, account_id=request.user
            ).delete()

        return redirect("profile")
