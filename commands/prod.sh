#!/bin/bash

#gunicorn -w 4 -b 0.0.0.0:8000 --chdir /srv/project/src settings.wsgi --timeout 10
gunicorn -w 4 app.wsgi:application --chdir /opt/project -b 0:$WSGI_PORT --log-level $LOG_LEVEL