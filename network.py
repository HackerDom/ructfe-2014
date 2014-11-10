#!/usr/bin/python

from socket import SOCK_STREAM, AF_INET, socket, SO_REUSEADDR, SOL_SOCKET
import thread

_author__ = 'm_messiah'


class Connection:
    def __init__(self, _conn, _addr):
        self.conn = _conn
        self.addr = _addr
        self.alive = True

    #def __getattr__(self, name):
    #    return getattr(self.conn, name)

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
                response = ""
                if not data:
                    break
                if "hello" in data:
                    response = "Hi there!"
                elif "wtf" in data:
                    response = "Just another sockserver"
                elif "bye" in data:
                    response = "bye, bye!"
                    self.alive = False

                self.sendline(response)

        except:
            pass
        finally:
            self.close()


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
            thread.start_new_thread(self.handler, (conn, addr))

    def handler(self, conn, addr):
        conn = Connection(conn, addr)
        conn.serve()
