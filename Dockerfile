# <--- BASE stage ---> #

FROM python:3.13 AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv 

WORKDIR /app

COPY pyproject.toml ./


# <--- TEST stage ---> #

FROM base AS test

RUN uv venv && uv sync

COPY . .

# <--- PROD stage ---> #

FROM base AS prod

RUN uv venv && uv sync --no-dev

RUN groupadd -r django_group && \
    useradd -G django_group -b /app -rM django_user

COPY --chown=django_user:django_group . .

USER django_user

CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:6789", "core.wsgi"]

