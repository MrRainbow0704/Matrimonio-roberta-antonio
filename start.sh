#!/usr/bin/env bash

echo "Starting gunicorn..."
source ./.venv/bin/activate
gunicorn -c ./config/gunicorn.py
sleep 5
tail /var/log/gunicorn/dev.log -n 15
deactivate
echo "Gunicorn started!"