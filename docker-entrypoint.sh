#!/bin/sh
set -e

if [ "$1" = "./run_controller.py" ] && [ "$(id -u)" = "0" ]; then
    chown -R resinapp .
    exec su-exec resinapp "$@"
fi

exec "$@"
