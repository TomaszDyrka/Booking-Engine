from __future__ import annotations

from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.core.validators import RegexValidator, EmailValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from enum import Enum, auto, unique
import re


class AccountManager(BaseUserManager):
    def check_admin_options(
            self,
            expected_superuser: bool,
            **fields,
            ):
        """ Checks if account is suitable for staff roles (admin and moderator)"""

        if fields.get("is_staff") is not True:
            raise ValueError("'is_staff' should be set to True")
        if fields.get("is_superuser") is not expected_superuser:
            raise ValueError(f"'is_superuser' should be set to {expected_superuser}, but is {fields.get('is_superuser')}")  # noqa: E501
        if fields.get("is_active") is not True:
            raise ValueError("'is_active' should be set to True")

    def check_required_fields(
            self,
            email: str,
            pesel: str,
            password: str,):
        """ Checks if required fields are provided """

        if not email:
            raise ValueError("No email provided!")

        if not pesel:
            raise ValueError("No pesel provided!")

        if not password:
            raise ValueError("No password provided!")

        if not re.match(r"^\d{11}$", pesel):
            raise ValueError("Pesel is wrong!")

        # Security checks

        # PASSWORD_PATTERN_DEF = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
        # PASSWORD_PATTERN_DIG = r"\d"
        # PASSWORD_PATTERN_UPC = r"[A-Z]"
        # PASSWORD_PATTERN_LWC = r"[a-z]"
        # PASSWORD_PATTERN_NUM = r"^.{8,}$"

        # if not re.search(PASSWORD_PATTERN_DIG, password):
        # raise ValueError("Password must contain at least one digit")
        # if not re.search(PASSWORD_PATTERN_UPC, password):
        # raise ValueError("Password must contain at least one uppercase letter")
        # if not re.search(PASSWORD_PATTERN_LWC, password):
        # raise ValueError("Password must contain at least one lowercase letter")
        # if not re.search(PASSWORD_PATTERN_NUM, password):
        # raise ValueError("Password must contain at least 8 characters")

    def create_user(
            self,
            email: str,
            pesel: str,
            password: str,
            **fields,):
        """ Creates and saves standard user """

        self.check_required_fields(email, pesel, password)

        email = self.normalize_email(email)
        user = self.model(email=email, pesel=pesel, **fields)
        grp = fields.setdefault("type", Account.AccountType.STANDARD)

        try:
            grp = Group.objects.get(name=fields.get("type"))
        except Group.DoesNotExist:
            raise ValueError(f"Group {fields.get("type")} does not exist!")

        user.set_password(password)
        user.save()

        user.groups.add(grp)

        return user

    def create_superuser(
            self,
            email: str,
            pesel: str,
            password: str,
            **fields,):
        """ Creates and saves superuser """

        fields.setdefault("is_staff", True)
        fields.setdefault("is_superuser", True)
        fields.setdefault("is_active", True)
        fields.setdefault("type", Account.AccountType.ADMIN)

        self.check_admin_options(True, **fields)

        return self.create_user(email, pesel, password, **fields)

    def create_moderator(
            self,
            email: str,
            pesel: str,
            password: str,
            **fields,):
        """ Creates and saves moderator """

        self.check_required_fields(email, pesel, password)

        fields.setdefault("is_staff", True)
        fields.setdefault("is_superuser", False)
        fields.setdefault("is_active", True)
        fields.setdefault("type", Account.AccountType.MODERATOR)

        self.check_admin_options(False, **fields)

        return self.create_user(email, pesel, password, **fields)


class Account(AbstractUser):
    class AccountType(models.TextChoices):
        STANDARD = "Standard", _("Standard")
        MODERATOR = "Moderators", _("Moderators")
        ADMIN = "Administrators", _("Administrators")

    username = None
    email = models.EmailField(
                    verbose_name=_("Email address"),
                    max_length=255,
                    unique=True,
                    validators=[EmailValidator(
                        message=_("Provided email is not valid!"),
                        )],
                    )

    first_name = models.CharField(
                    verbose_name=_("First name"),
                    max_length=255,
                    )

    last_name = models.CharField(
                    verbose_name=_("Last name"),
                    max_length=255,
                    )

    pesel = models.CharField(
                    verbose_name=_("Pesel"),
                    unique=True,
                    validators=[RegexValidator(
                        regex=r'^\d{11}$',
                        message=_('PESEL has to have 11 digits!'),
                        )],
                    )

    type = models.CharField(
                    verbose_name=_("Account type"),
                    max_length=255,
                    choices=AccountType,
                    default=AccountType.STANDARD,
                    )

    creation_date = models.DateField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["pesel"]

    objects = AccountManager()

    class Meta():
        verbose_name = "account"
        verbose_name_plural = "accounts"
        abstract = False

    @property
    def is_admin(self):
        return self.is_superuser

    @property
    def is_moderator(self):
        return self.is_staff and not self.is_superuser

    def __str__(self):
        return f"{self.email} : {self.first_name} {self.last_name}"
