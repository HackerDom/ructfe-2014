__author__ = 'pahaz'


def secret(req):
    print(repr(req))
    return 200, "O-LO-LO"
