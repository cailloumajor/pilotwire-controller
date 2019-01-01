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

ARG PIFACECOMMON_REF=ff3cd937b7da2e8b60ebde65457c089427661812
ARG PIFACEDIGITALIO_REF=d231a82bdb55d5f57f44ba7aec00bfd6c0b9a9d4
# hadolint ignore=DL3018
RUN set -ex \
    && apk add --no-cache --virtual .git-for-pip \
        git \
    && pip install \
        "git+https://github.com/piface/pifacecommon@${PIFACECOMMON_REF}#egg=pifacecommon" \
        "git+https://github.com/piface/pifacedigitalio@${PIFACEDIGITALIO_REF}#egg=pifacedigitalio" \
    && apk del --no-cache .git-for-pip

WORKDIR /usr/src/app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

COPY ./ .

RUN mv docker-entrypoint.sh /usr/local/bin
ENTRYPOINT ["/sbin/tini", "--", "docker-entrypoint.sh"]

CMD ["./run_controller.py", "--port", "17171"]
