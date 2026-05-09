from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Account


class CustomAccountCreationForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ("email", "pesel",)


class CustomAccountChangeForm(UserChangeForm):

    class Meta:
        model = Account
        fields = ("email",)
