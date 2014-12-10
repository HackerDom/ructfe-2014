#!/usr/bin/python
#  coding=utf-8
__author__ = 'm_messiah'
import socket
from sys import argv, exit, stderr
import os


def check(hostname):
    try:
        response = os.system("ping -c 1 -t 3 " + hostname + " > /dev/null 2>&1")
        if response != 0:
            print "Host unreachable"
            return 104

        sock = socket.socket()
        sock.connect((hostname, 2707))
        sock.sendall("Question\n")
        data = sock.recv(20)
        sock.close()
        if "42" in data:
            return 101
        else:
            print "Bad Answer"
            return 103
    except socket.error as e:
        print "Port unreachable"
        return 104


def put(hostname, id, flag):
    try:
        sock = socket.socket()
        sock.connect((hostname, 2707))
        sock.sendall("register {0}".format(id))
        token = sock.recv(128).strip()
        sock.sendall("add {0} {1}".format(token, flag))
        data = sock.recv(1024)
        if "stored:" in data:
            sock.close()
            print token
            return 101
        else:
            stderr.write("Bad answer: {0}".format(data))
            return 103
    except socket.error:
        return check(hostname)


def get(hostname, id, flag):
    try:
        sock = socket.socket()
        sock.connect((hostname, 2707))
        sock.sendall("view {0} 10".format(id))
        data = sock.recv(1024)
        if flag in data:
            sock.close()
            return 101
        else:
            sock.sendall("view {0} 50".format(id))
            data = sock.recv(10240)
            sock.close()
            if flag in data:
                return 101
            else:
                return 102
    except socket.error:
        return check(hostname)


if __name__ == '__main__':
    if len(argv) > 1:
        if argv[1] == "check":
            if len(argv) > 2:
                exit(check(argv[2]))
        elif argv[1] == "put":
            if len(argv) > 4:
                exit(put(argv[2], argv[3], argv[4]))
        elif argv[1] == "get":
            if len(argv) > 4:
                exit(get(argv[2], argv[3], argv[4]))
    exit(110)
