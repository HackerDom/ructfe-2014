#!/usr/bin/python3

import asyncore
from collections import OrderedDict


class LimitedSizeDict(OrderedDict):
    LIMIT = 100000

    def __init__(self, *args, **kwds):
        OrderedDict.__init__(self, *args, **kwds)
        self._check_size_limit()

    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()

    def _check_size_limit(self):
        while len(self) > self.LIMIT:
            self.popitem(last=False)

flags = LimitedSizeDict()


class FlagHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(8192)

        try:
            cmd, flag_id, flag = data.strip().split(maxsplit=2)
            if cmd == b"put":
                flags[flag_id] = flag
                self.send(b"+ ok\n")
            elif cmd == b"check":
                if flag_id in flags:
                    if flag == flags[flag_id]:
                        self.send(b"+ ok\n")
                    else:
                        self.send(b"- err\n")
                else:
                    self.send(b"- no such flag\n")
            else:
                raise(Exception())

        except Exception:
            self.send(b"- wrong command\n")


class FlagServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(100)

    def handle_accepted(self, sock, addr):
        print('Incoming connection from %s' % repr(addr))
        FlagHandler(sock)

server = FlagServer('0.0.0.0', 31337)
asyncore.loop()
