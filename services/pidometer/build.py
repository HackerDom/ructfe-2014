#!/usr/bin/python
__author__ = 'm_messiah'

from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='Pidometer',
    ext_modules=cythonize("network.pyx"),
)
