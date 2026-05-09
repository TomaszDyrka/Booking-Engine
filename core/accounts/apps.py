from django.apps import AppConfig
from django.db.models.signals import post_migrate

def make_groups(sender, **kwagrs):
    from django.contrib.auth.models import Group, Permission

    # ADMIN
    try:
        Group.objects.get(name="Administrators")

    except Group.DoesNotExist:
        group = Group.objects.create(name="Administrators")
        perms = Permission.objects.filter(codename__regex=r'^(view|change|add|delete)_')
        group.permissions.set(perms)

    # MODERATOR
    try:
        Group.objects.get(name="Moderators")

    except Group.DoesNotExist:
        group = Group.objects.create(name="Moderators")
        perms = Permission.objects.filter(codename__regex=r'^(view|change)_')
        group.permissions.set(perms)

    # STANDARD
    try:
        Group.objects.get(name="Standard")

    except Group.DoesNotExist:
        group = Group.objects.create(name="Standard")
        perms = Permission.objects.filter(codename__startswith="view_")
        group.permissions.set(perms)

class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        post_migrate.connect(make_groups, sender=self)
