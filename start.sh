#! /usr/bin/bash
source .venv/bin/activate
gunicorn -c config/gunicorn.py
echo "Gunicorn started!"
tail /var/log/gunicorn/dev.log -n 5