#! /usr/bin/bash
source .venv/bin/activate
gunicorn -c config/gunicorn.py
echo "Gunicorn started!"