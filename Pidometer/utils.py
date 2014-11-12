# -*- coding: utf-8 -*-
__author__ = 'muzafarov'

from cutils import distanceCoords

def spark(ints):
    """Returns a spark string from given iterable of ints.
    github.com/kennethreitz/spark.py
    """
    ticks = u' ▁▂▃▄▅▆▇█'
    step = (max(ints) / float(len(ticks) - 1)) or 1
    return u''.join(ticks[int(round(i / step))] for i in ints)


def ctoi(c):
    flag = u"abcdefghijklmnopqrstuvwxyz1234567890"
    return flag.index(c) + 24


def createPath(flag):
    # Flag is: ^\w{31}=
    # So, abcdefghijklmnopqrstuvwxyz12345= is a flag,
    # and 'abc' is a lattitude (a.bc),
    # 'efg' is a longitude (e.fg)
    # and every next char pair is a delta of (lat,long) for a 2 hours.
    flag = flag[:31]
    coords = [(float("{0}.{1}{2}".format(*map(ctoi, flag[:3]))),
               float("{0}.{1}{2}".format(*map(ctoi, flag[4:7]))))]
    for i in range(7, 31, 2):
        coords.append((coords[-1][0] + ctoi(flag[i]) / 1000.,
                       coords[-1][1] + ctoi(flag[i + 1]) / 1000.))
    return coords


def parsePath(path, step=1.0):
    # We have a GPS, so it is good to calculate steps, through steplength.
    try:
        if len(path) < 13:
            return 1
        distances = [distanceCoords(path[i-1], path[i]) / step
                     for i in range(1, 13)]
        return distances
    except:
        return 2