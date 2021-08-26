FROM python:3.9 as base
LABEL maintainer "Thiago Pacheco <hi@pacheco.io>"
RUN apt-get update
WORKDIR /usr/src/app

ENV ENVIRONMENT=development

ENV ENVIRONMENT=${ENVIRONMENT} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.0 \
  FLASK_ENV="docker" \
  FLASK_APP=main.py
# System deps:
RUN pip3 install -U "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml ./

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$ENVIRONMENT" == production && echo "--no-dev") --no-interaction --no-ansi

EXPOSE 5000
CMD poetry run python main.py

FROM base as prod
COPY . .
CMD ["gunicorn", "--reload", "--bind", "0.0.0.0:5000", "app:app"]