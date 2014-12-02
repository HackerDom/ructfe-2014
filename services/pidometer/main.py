#!/usr/bin/python
# coding=utf-8
__author__ = 'm_messiah'

from network import *

if __name__ == '__main__':
    S = Server("", 27001)
    S.serve()