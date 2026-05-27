import getpass
import re
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email
from django.contrib.auth import get_user_model

Account = get_user_model()


class Command(BaseCommand):
    help = "Creates moderator account"

    def handle(self, *args, **options):
        try:
            # email
            while True:
                try:
                    email = input("Email address: ")
                    validate_email(email)
                    break

                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(e.message))

            # pesel
            while True:
                try:
                    pesel = input("Pesel: ")
                    if not re.match(r"^\d{11}$", pesel):
                        raise ValueError
                    break

                except ValueError:
                    self.stdout.write(self.style.ERROR("PESEL has to have 11 digits!"))

            # password
            while True:
                try:
                    password = getpass.getpass("Password: ")
                    password_confirm = getpass.getpass("Password (again): ")

                    assert password == password_confirm
                    break

                except AssertionError:
                    self.stdout.write(
                        self.style.ERROR("Error: Your passwords didn't match")
                    )

        except (KeyboardInterrupt, EOFError):
            self.stdout.write(self.style.ERROR("\nOperation cancelled."))
            return

        try:
            Account.objects.create_moderator(
                email=email,
                pesel=pesel,
                password=password,
            )
            self.stdout.write(self.style.SUCCESS("\nModerator created successfully"))

        except ValueError as e:
            raise CommandError(f"Value Error: {e}")
