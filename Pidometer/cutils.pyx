__author__ = 'muzafarov'
from math import acos, sin, cos, pi, sqrt, pow, atan2

def distanceCoords(tuple start, tuple end):
    cdef tuple r_start, r_end
    cdef double cl1, cl2, sl1, sl2, delta, cdt, sdt
    cdef double x, y, ad
    cdef double rad = pi / 180.0
    cdef long dist
    r_start = (start[0] * rad, start[1] * rad)
    r_end = (end[0] * rad, end[1] * rad)
    cl1 = cos(r_start[0])
    cl2 = cos(r_end[0])
    sl1 = sin(r_start[0])
    sl2 = sin(r_end[0])
    dt = r_end[1] - r_start[1]
    cdt = cos(dt)
    sdt = sin(dt)
    y = sqrt(pow(cl2 * sdt, 2) + pow(cl1 * sl2 - sl1 * cl2 * cdt, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdt
    ad = atan2(y, x)
    dist = int(ad * 6372795)
    return dist
