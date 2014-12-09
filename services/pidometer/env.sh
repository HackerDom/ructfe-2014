#!/bin/bash

pkgadd -d http://get.opencsw.org/now
/opt/csw/bin/pkgutil -U
/opt/csw/bin/pkgutil -i libmcrypt4 mcrypt_dev redis
pkg install SUNWhea SUNWarc SUNWlibm SUNWlibms SUNWdfbh  SUNWlibC SUNWzlib gcc-43 wget gnu-make
export CPPFLAGS="-I/opt/csw/include"
export LDFLAGS="-L/opt/csw/lib -R/opt/csw/lib"
export PKG_CONFIG_PATH="/opt/csw/lib/pkgconfig"

easy_install redis hiredis python-mcrypt
# PYTHONPATH=. ./Server
