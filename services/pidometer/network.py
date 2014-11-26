#!/usr/bin/python

from socket import SOCK_STREAM, AF_INET, socket, SO_REUSEADDR, SOL_SOCKET
import thread
from mcrypt import MCRYPT
import base64 as base
from cutils import to_human_day
import redis
from utils import *


_author__ = 'm_messiah'
db = redis.StrictRedis(host='r14-test4-1.urgu.org', port=6379, db=0)
crypter = MCRYPT("gost", "ecb")
# TODO: how to generate key?
crypter.init("0" * 32)


def add_path(token, path, end=""):
    try:
        steps = parsePath(createPath(path))
        db.lpush(token, path)
        step_all = spark(steps) + "\t" + str(sum(steps))
        db.lpush(get_name(token), step_all)
        return step_all
    except Exception as e:
        db.lpop(token)
        return "Invalid token" + str(e)


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
    if count == 0:
        day, count = count, day
    return u"\n".join(
        [name + u" steps:"] +
        [to_human_day(i) + u":\t\t" + v.decode("utf8")
         for i, v in enumerate(db.lrange(name, day, count))]
    )


class Connection:
    def __init__(self, _conn, _addr):
        self.conn = _conn
        self.addr = _addr
        self.alive = True
        self.commands = {
            "add": add_path,
            "register": register,
            "view": view_user,
        }

    def recvline(self):
        return self.conn.recv(256)

    def sendline(self, line):
        line += "\r\n"
        self.conn.sendall(line)

    def close(self):
        try:
            self.sendline("-" * 20)
        except:
            pass  # Connection already closed
        finally:
            self.conn.close()

    def serve(self):
        try:
            while self.alive:
                data = self.recvline()
                if not data:
                    break
                if u"quit" in data:
                    response = u"bye, bye!"
                    self.alive = False
                else:
                    command = data.split()
                    try:
                        response = unicode(
                            self.commands[command[0].lower()](*command[1:])
                            if command[0] in self.commands
                            else "Unknown command"
                        )
                    except ValueError as e:
                        response = "Bad data" + str(e)
                    except IndexError:
                        response = "Not enough data"
                self.sendline(response.encode("utf-8"))

            self.close()

        except Exception as e:
            print e
        finally:
            self.close()


def handler(conn, addr):
    conn = Connection(conn, addr)
    conn.serve()


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def serve(self):
        self.socket.bind((self.host, self.port))
        while True:
            self.socket.listen(100)
            conn, addr = self.socket.accept()
            thread.start_new_thread(handler, (conn, addr))


if __name__ == "__main__":
    S = Server("", 27001)
    S.serve()