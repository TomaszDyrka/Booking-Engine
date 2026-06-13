from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, ProfileListView

urlpatterns = [
    path("registrations/", RegisterView.as_view(template_name="registrations/register.html"), name="register"),
    path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileListView.as_view(template_name="accounts/profile.html"), name="profile")
]