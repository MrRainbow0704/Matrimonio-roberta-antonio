"""Gunicorn config file"""

from . import HOST, PORT, DEBUG

# WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "app:app"
# The granularity of Error log outputs
loglevel = "debug"
# The number of worker processes for handling requests
workers = 5
# The socket to bind
bind = f"{HOST}:{PORT}"
# Restart workers when code changes (development only!)
reload = DEBUG
# Write access and error info to /var/log
accesslog = errorlog = "/var/log/gunicorn/dev.log"
# Redirect stdout/stderr to log file
capture_output = True
# PID file so you can easily fetch process ID
pidfile = "/var/run/gunicorn/dev.pid"
# Daemonize the Gunicorn process (detach & enter background)
daemon = True
# Avoid timeout errors
timeout = 90
