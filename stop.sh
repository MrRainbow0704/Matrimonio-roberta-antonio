#! /usr/bin/bash
cat /var/run/gunicorn/dev.pid | xargs kill -9
echo "Gunicorn killed!"