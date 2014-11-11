# -*- coding: utf-8 -*-
__author__ = 'muzafarov'

def spark(ints):
    """Returns a spark string from given iterable of ints.
    github.com/kennethreitz/spark.py
    """
    ticks = u' ▁▂▃▄▅▆▇█'
    step = (max(ints) / float(len(ticks) - 1)) or 1
    return u''.join(ticks[int(round(i / step))] for i in ints)
