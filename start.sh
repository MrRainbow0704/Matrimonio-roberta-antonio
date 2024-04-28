#!/usr/bin/env bash

echo "Starting gunicorn..."
source ./.venv/bin/activate
gunicorn -c ./config/__init__.py
sleep 5
tail /var/log/gunicorn/dev.log -f
deactivate
echo "Gunicorn started!"