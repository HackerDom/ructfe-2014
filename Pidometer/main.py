#!/usr/bin/python
__author__ = 'm_messiah'

from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='Hello world app',
    ext_modules=cythonize("cutils.pyx"),
)
