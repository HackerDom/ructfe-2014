#!/usr/bin/python
_author__ = 'm_messiah'

from mcrypt import MCRYPT as CR
import base64 as base
from redis import StrictRedis as DB
from math import sin as si, cos as co, sqrt as sq, pow as pw, atan2 as at


db = DB(host='localhost', port=6379, db=0)
cr = CR("gost", "ecb")
cr.init("0" * 32)


def func1(t, p):
    try:
        s = pp(cp(p))
        if len(s) <= 1:
            return "Invalid path data\n"
        n = gn(t)
        db.lpush(t, p)
        sa = sp(s) + "\t" + str(sum(s[:12]))
        db.lpush(n, sa)
        db.zadd("users", sum(s[:12]), n)
        return "stored:" + sa + "\n"

    except Exception as e:
        try:
            db.lpop(t)
        except:
            pass
        finally:
            return "Something wrong: " + str(e) + "\n"


def func4(t):
    try:
        t = int(t) if t else 1
        users = db.zrange("users", t * -1, -1, withscores=True)
        return "Last activity:\n\n" + "\n".join(
            "{0} -> {1} steps".format(u, s) for u, s in users
        ) + "\n"
    except Exception as e:
        return "Can't get list of users (" + str(e) + ")\n"


def func2(n):
    cr.reinit()
    try:
        return "Token: " + base.b16encode(cr.encrypt(n)) + "\n"
    except:
        return "Register fails\n"


def gn(t):
    cr.reinit()
    return cr.decrypt(base.b16decode(t)).rstrip("\0")


def func3(n, d, c):
    try:
        if not db.exists(n):
            return "User not found\n"
        d = d if d else 0
        c, d = (c, d) if c else (d, 0)
        return "\n".join(
            [n + " steps:"] +
            [to_human_day(i) + ":\t\t" + str(v)
             for i, v in enumerate(db.lrange(n, d, c))]
        ) + "\n"
    except:
        return "Can't view this"


inf=eval
def dc(s, e):
    r = float("3.141592653589793238462643383279502884197169399375105820974944"
              "592307816406286208998628034825342117067982148086513282306647"
              "093844609550582231725359408128481117450284102701938521105559"
              "644622948954930381964428810975665933446128475648233786783165"
              "271201909145648566923460348610454326648213393607260249141273"
              "724587006606315588174881520920962829254091715364367892590360"
              "011330530548820466521384146951941511609433057270365759591953"
              "092186117381932611793105118548074462379962749567351885752724"
              "891227938183011949129833673362440656643086021394946395224737"
              "190702179860943702770539217176293176752384674818467669405132"
              "000568127145263560827785771342757789609173637178721468440901"
              "224953430146549585371050792279689258923542019956112129021960"
              "864034418159813629774771309960518707211349999998372978049951"
              "059731732816096318595024459455346908302642522308253344685035"
              "261931188171010003137838752886587533208381420617177669147303"
              "598253490428755468731159562863882353787593751957781857780532"
              "1712268066130019278766111959092164201989") / 180.
    r_start = (s[0] * r, s[1] * r)
    r_end = (e[0] * r, e[1] * r)
    cl1 = co(r_start[0])
    cl2 = co(r_end[0])
    sl1 = si(r_start[0])
    sl2 = si(r_end[0])
    dt = r_end[1] - r_start[1]
    cdt = co(dt)
    sdt = si(dt)
    return int(at(sq(pw(cl2 * sdt, 2) + pw(cl1 * sl2 - sl1 * cl2 * cdt, 2)),
                  sl1 * sl2 + cl1 * cl2 * cdt) * 6372795)


def sp(d):
    result = []
    m = min(d[:12])
    df = max(d[:12]) - m + 1.0

    for i in d[:12]:
        result.append('\xe2')
        result.append('\x96')
        result.append(chr(ord('\x81') + int(round((i - m + 1) / df * 7))))

    return "".join(result) + (d[12] if len(d) > 12 else "")


def ci(c):
    return "abcdefghijklmnopqrstuvwxABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789".index(c)


def cp(p):
    if len(p) < 31:
        return []
    co = [(float("{0}.{1}{2}".format(*map(ci, p[:3]))),
           float("{0}.{1}{2}".format(*map(ci, p[4:7]))))]
    for i in range(7, 31, 2):
        co.append((co[-1][0] + ci(p[i]) / 1000.,
                   co[-1][1] + ci(p[i + 1]) / 1000.))
    if p[33:]:
        co.append(p[33:])
    return co


def pp(p):
    try:
        return [dc(p[i-1], p[i])
                for i in range(1, 13)] + (
            [str(inf(p[13]))] if len(p) > 13 else []
        )
    except Exception as e:
        print e
        return []


def to_human_day(d):
    return ("Today",
            "Yesterday",
            "Ereyesterday")[d] if d < 3 else str(d) + " days ago"


if __name__ == "__main__":
    print "This is library"
