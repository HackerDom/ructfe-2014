#!/usr/bin/python
__author__ = 'm_messiah'

from network import *
from random import randint

if __name__ == '__main__':
    a = chr(randint(65, 90))
    print ">register messiah"
    print "<" + register("messiah"),
    print ">add 87B21AC53239244D BKL51GFZFIUWV86FWWGFZTOTI1DQXF{0}=".format(a)
    print "<" + add_path("87B21AC53239244D",
                         "BKL51GFZFIUWV86FWWGFZTOTI1DQXF{0}=".format(a)),
    print ">view messiah"
    print "<" + view_user("messiah", None, None),
    print ">view 87B21AC53239244D"
    print "<" + view_user("87B21AC53239244D", None, None),