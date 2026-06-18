#!/bin/bash

uv run python manage.py migrate

# || true just for the case if admin was already there
DJANGO_SUPERUSER_PASSWORD=1234 \
uv run python manage.py createsuperuser \
--noinput --email=admin@test.com --pesel=12312312312 || true

exec "$@"
