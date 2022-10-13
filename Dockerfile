# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.9-buster

# Add user that will be used in the container.
ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

RUN set -ex \
    && RUN_DEPS=" \
    libpcre3 \
    mime-support \
    postgresql-client \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Copy in your requirements file
ADD requirements /requirements

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    libpcre3-dev \
    libpq-dev \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install --no-cache-dir -r /requirements/requirements.txt \
    && pip install "gunicorn==20.1.0" \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*


# Use /app folder as a directory where the source code is stored.
RUN mkdir -p /app/static
WORKDIR /app

RUN chown -R ${APP_USER}:${APP_USER} /app

# Copy the source code of the project into the container.
COPY --chown=${APP_USER}:${APP_USER} . .

USER ${APP_USER}

ENV DJANGO_SETTINGS_MODULE=settings.production

# ENTRYPOINT ["/app/docker/docker-entrypoint.sh"]
# CMD ["python3", "-m", "http.server"]

EXPOSE 8000
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "neusler.wsgi",]