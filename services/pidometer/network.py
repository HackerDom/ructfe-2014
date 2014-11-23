#!/usr/bin/pythonw

from socket import SOCK_STREAM, AF_INET, socket, SO_REUSEADDR, SOL_SOCKET
from utils import *
import thread
import mcrypt


_author__ = 'm_messiah'


def add_path(path, end=""):
    steps = parsePath(createPath(path))
    # Write to DB
    return spark(steps) + "\t" + str(sum(steps)) + "\n" + str(steps) + end


def register(name):
    def create_token(name_):
        return u"hello_{}".format(name_)
    token = create_token(name)
    # create db/dir/something else
    return token


class Connection:
    def __init__(self, _conn, _addr):
        self.conn = _conn
        self.addr = _addr
        self.alive = True
        self.commands = {
            "add": add_path,
            "register": register,
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
            while True:
                if not self.alive:
                    self.close()

                data = self.recvline()
                if not data:
                    break
                if u"quit" in data:
                    response = u"bye, bye!"
                    self.alive = False
                else:
                    command = data.lower().split()
                    try:
                        response = unicode(
                            self.commands[command[0]](*command[1:])
                            if command[0] in self.commands
                            else "Unknown command"
                        )
                    except ValueError:
                        response = "Bad data"
                    except IndexError:
                        response = "Not enough data"
                self.sendline(response.encode("utf-8"))

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