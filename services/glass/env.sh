#!/bin/bash

pkgadd -d http://get.opencsw.org/now
/opt/csw/bin/pkgutil -U
/opt/csw/bin/pkgutil -i -y python33 py_virtualenv

# INSTALL NGINX WITH nginx.cfg

virtualenv --python=python3 venv
source ./venv/bin/activate
pip install gunicorn
gunicorn wsgi:application --bind 127.0.0.1:8001 &> gunicorn.log

# gunicorn wsgi:application --bind 0.0.0.0:8001 &> gunicorn.log
