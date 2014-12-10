#!/usr/bin/env python3

import os
import socket
import sys
import traceback
import re

PORT = 2222
TIMEOUT = 30
CONNECT_TIMEOUT = 5

REPEATS = 1
NOP_COUNT = 1

MSG_OUT_SIZE = 1
MSG_OUT_SIZE_DT = 0

OK, CORRUPT, MUMBLE, DOWN, CHECKER_ERROR = 101, 102, 103, 104, 110


def readline(s):
    chars = []
    while True:
        a = s.recv(1)
        chars.append(a)
        if not a or a == b"\n":
            return b"".join(chars)


def pad_and_send(s, msg, flags_num=0):
    l = int(MSG_OUT_SIZE + MSG_OUT_SIZE_DT * flags_num)
    if len(msg) < l:
        msg += " " + "A" * (l - len(msg) - 1)
    msg += "\n"
    s.sendall(msg.encode())


def check(host):
    try:
        socket.create_connection((host, PORT), CONNECT_TIMEOUT)
        s.settimeout(TIMEOUT)
    except Exception:
        return DOWN
    else:
        return OK


def put(host, flag_id, flag):
    try:
        s = socket.create_connection((host, PORT), CONNECT_TIMEOUT)
        s.settimeout(TIMEOUT)
    except Exception:
        return DOWN

    try:
        hello_re = rb"\+ I've got (\d+) flags"
        flags_num = int(re.match(hello_re, readline(s).strip()).group(1))

        for i in range(NOP_COUNT):
            pad_and_send(s, "nop", flags_num)
            readline(s)
    
        pad_and_send(s, "put %s %s" % (flag_id, flag), flags_num)

        if readline(s)[0] != ord("+"):
            return MUMBLE

        return OK
    except Exception:
        traceback.print_exc()
        return MUMBLE


def get(host, flag_id, flag):
    try:
        s = socket.create_connection((host, PORT), CONNECT_TIMEOUT)
        s.settimeout(TIMEOUT)
    except Exception:
        return DOWN

    try:
        hello_re = rb"\+ I've got (\d+) flags"
        flags_num = int(re.match(hello_re, readline(s).strip()).group(1))

        for i in range(NOP_COUNT):
            pad_and_send(s, "nop", flags_num)
            readline(s)

        pad_and_send(s, "get %s" % flag_id, flags_num)

        if flag.encode() not in readline(s):
            return CORRUPT

        return OK
    except Exception:
        traceback.print_exc()
        return MUMBLE


def main(argv):
    cmds = {"check": check, "put": put, "get": get}
    for i in range(REPEATS - 1):
        cmds[argv[0]](*argv[1:])
    return cmds[argv[0]](*argv[1:])

if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception:
        traceback.print_exc()
        sys.exit(CHECKER_ERROR)
