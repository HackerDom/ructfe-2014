#!/usr/bin/python
# coding=utf-8
__author__ = 'm_messiah'

from network import *

if __name__ == '__main__':
    print ">register messiah"
    print "<" + register(u"messiah")
    print ">add 87B21AC53239244D 7al10jy3oyn5w5rn4z74nqyb7yfpy4b="
    print "<" + add_path(u"87B21AC53239244D",
                         u"7al10jy3oyn5w5rn4z74nqyb7yfpy4b=")
    print ">view messiah"
    print "<" + view_user(u"messiah")
    print ">view 87B21AC53239244D"
    print "<" + view_user(u"87B21AC53239244D")