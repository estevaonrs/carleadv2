#!/usr/bin/env bash

set -e

# Usage: wait-for-it.sh host:port [-t timeout] [-- command args]
# Will wait for a host:port to be available before executing the command.

TIMEOUT=15
WAIT_FOR=""
CMD=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        *:* )
            WAIT_FOR="$1"
            shift
            ;;
        -t)
            shift
            TIMEOUT="$1"
            shift
            ;;
        --)
            shift
            CMD="$@"
            break
            ;;
        *)
            echo "Invalid argument: $1"
            exit 1
            ;;
    esac
done

if [ -z "$WAIT_FOR" ]; then
    echo "Error: No host:port supplied"
    exit 1
fi

HOST=$(echo "$WAIT_FOR" | cut -d: -f1)
PORT=$(echo "$WAIT_FOR" | cut -d: -f2)

for i in $(seq $TIMEOUT); do
    if nc -z "$HOST" "$PORT" >/dev/null 2>&1; then
        echo "$HOST:$PORT is available!"
        break
    fi
    echo "Waiting for $HOST:$PORT..."
    sleep 1
done

if ! nc -z "$HOST" "$PORT" >/dev/null 2>&1; then
    echo "Timeout waiting for $HOST:$PORT"
    exit 1
fi

if [ -n "$CMD" ]; then
    exec "$CMD"
fi
