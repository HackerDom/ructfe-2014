# coding=utf-8
_author__ = 'm_messiah'

from mcrypt import MCRYPT
import base64 as base
import redis
from math import sin, cos, pi, sqrt, pow, atan2


db = redis.StrictRedis(host='r14-test4-1.urgu.org', port=6379, db=0)
crypter = MCRYPT("gost", "ecb")
# TODO: how to generate key?
crypter.init("0" * 32)


def add_path(token, path):
    try:
        steps = parsePath(createPath(path))
        db.lpush(token, path)
        step_all = spark(steps) + "\t" + str(sum(steps))
        db.lpush(get_name(token), step_all)
        return step_all
    except Exception as e:
        db.lpop(token)
        return u"Invalid token: " + str(e)


def register(name):
    token = get_token(name)
    # Security fix:
    # if db.exists(token):
    #     return "Name exists"
    return token


def get_token(name_):
    crypter.reinit()
    return base.b16encode(crypter.encrypt(name_))


def get_name(token):
    crypter.reinit()
    return crypter.decrypt(base.b16decode(token)).rstrip("\0")


def view_user(name, day=0, count=0):
    if not db.exists(name):
        return "User not found"
    day = int(day)
    count = int(count)
    if count == 0:
        day, count = count, day
    return u"\n".join(
        [name + u" steps:"] +
        [to_human_day(i) + u":\t\t" + v.decode("utf8")
         for i, v in enumerate(db.lrange(name, day, count))]
    )


def distanceCoords(start, end):
    rad = pi / 180.0
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


def spark(ints):
    ticks = u' ▁▂▃▄▅▆▇█'
    step = (max(ints) / float(len(ticks) - 1)) or 1
    return u''.join(ticks[int(round(i / step))] for i in ints)


def ctoi(c):
    return u"abcdefghijklmnopqrstuvwxyz1234567890".index(c) + 24


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


def to_human_day(day):
    days = ("Today",
            "Yesterday",
            "Ereyesterday")
    if day < 3:
        return days[day]
    else:
        return str(day) + " days ago"


if __name__ == "__main__":
    print "This is library"
