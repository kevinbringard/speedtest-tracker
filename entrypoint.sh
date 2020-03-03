#!/bin/bash
set -e

# Prepend "SpeedTest" if the first argument is not an executable
if ! type -- "$1" &> /dev/null; then
	set -- /SpeedTest "$@"
fi

exec "$@"
