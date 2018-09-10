FROM arm32v6/alpine:3.8

LABEL maintainer="Arnaud Rocher <arnaud.roche3@gmail.com>"

ENV PIP_DEFAULT_TIMEOUT=60 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    PIPENV_COLORBLIND=true \
    PIPENV_HIDE_EMOJIS=true \
    PIPENV_NOSPIN=true \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1

ENV PYTHON_VER=3.6
# hadolint ignore=DL3013,DL3018
RUN set -ex \
    && addgroup -g 9999 resinapp \
    && adduser -S -u 9999 -G resinapp resinapp \
    && apk add --no-cache \
        git \
        "python3~=${PYTHON_VER}" \
        su-exec \
        tini \
    && pip${PYTHON_VER} install --upgrade pip \
    && pip${PYTHON_VER} install pipenv

WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system

ARG PIFACECOMMON_REF=ff3cd937b7da2e8b60ebde65457c089427661812
ARG PIFACEDIGITALIO_REF=d231a82bdb55d5f57f44ba7aec00bfd6c0b9a9d4
RUN set -ex \
    && pip${PYTHON_VER} install \
        "git+https://github.com/piface/pifacecommon@${PIFACECOMMON_REF}#egg=pifacecommon" \
        "git+https://github.com/piface/pifacedigitalio@${PIFACEDIGITALIO_REF}#egg=pifacedigitalio"

COPY ./ .
RUN python${PYTHON_VER} -m compileall pilotwire_controller

COPY docker-entrypoint.sh /usr/local/bin
ENTRYPOINT ["/sbin/tini", "--", "docker-entrypoint.sh"]

CMD ["./run_controller.py", "--port", "17171"]
