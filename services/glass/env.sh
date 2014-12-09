#!/bin/bash

pkgadd -d http://get.opencsw.org/now
/opt/csw/bin/pkgutil -U
/opt/csw/bin/pkgutil -i -y python33 py_virtualenv


