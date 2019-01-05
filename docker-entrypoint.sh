#!/bin/sh
set -e

# Fix permissions to use SPI
chown -R root:balena-app /dev/spidev*
chmod g+rw /dev/spidev*

if [ "$1" = "./run_controller.py" ] && [ "$(id -u)" = "0" ]; then
    chown -R balena-app .
    exec su-exec balena-app "$@"
fi

exec "$@"
