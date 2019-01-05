FROM arm32v6/python:3.7-alpine3.8

LABEL maintainer="Arnaud Rocher <arnaud.roche3@gmail.com>"

ENV PIP_DEFAULT_TIMEOUT=60 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1

# hadolint ignore=DL3013,DL3018
RUN set -ex \
    && addgroup -g 9999 balena-app \
    && adduser -S -u 9999 -G balena-app balena-app \
    && apk add --no-cache \
        su-exec \
        tini \
    && pip install poetry \
    && poetry config settings.virtualenvs.create false

WORKDIR /usr/src/app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

COPY ./ .

RUN mv docker-entrypoint.sh /usr/local/bin
ENTRYPOINT ["/sbin/tini", "--", "docker-entrypoint.sh"]

CMD ["./run_controller.py", "--port", "17171"]
