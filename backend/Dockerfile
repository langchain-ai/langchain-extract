# All directory paths for COPY commands are relative to the build context

# Ensure this python version stays in sync with CI
FROM python:3.11-slim as base
WORKDIR /backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME="/opt/poetry"
ENV MYPYPATH="/app/src/stubs"

# Use bash as the shell for the build
# https://github.com/docker/for-linux/issues/408#issuecomment-414748815
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN set -eux && \
    apt-get update && \
    apt-get install -y \
      build-essential \
      curl \
      libpq-dev \
      python3-dev \
      libmagic1

# https://python-poetry.org/docs
RUN pip install poetry

# install deps before copying project files so the cache is only invalidated
# when the deps change
COPY ./backend/pyproject.toml ./backend/poetry.lock .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --only main

COPY ./backend .

EXPOSE 8000

###
# development image
###
FROM base as development

ENTRYPOINT ["bash", "./scripts/local_entry_point.sh"]
