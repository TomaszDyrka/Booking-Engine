from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomAccountChangeForm, CustomAccountCreationForm
from .models import Account


class AccountAdmin(UserAdmin):
    add_form = CustomAccountCreationForm
    form = CustomAccountChangeForm
    model = Account

    list_display = ("email", "is_staff", "is_superuser", "is_active")
    list_filter = ("email", "is_staff", "is_superuser", "is_active")

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_superuser",
                "is_active", "groups", "user_permissions",
                )}
            ),
        )

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": (
            "is_superuser", "is_active", "groups", "user_permissions"
            )}
        ),
    )

    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(Account, AccountAdmin)
