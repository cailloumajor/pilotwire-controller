#!/bin/sh
set -e

# Fix permissions to use SPI & GPIO
chown -R root:resinapp /dev/spidev* /sys/class/gpio
chmod g+rw /dev/spidev*
chmod g+w /sys/class/gpio/*export

if [ "$1" = "./run_controller.py" ] && [ "$(id -u)" = "0" ]; then
    chown -R resinapp .
    exec su-exec resinapp "$@"
fi

exec "$@"
