#!/usr/bin/python3.4

from collections import OrderedDict
import asyncio
import sys

PORT = int(sys.argv[1])
MSG_OUT_SIZE = int(sys.argv[2])
MSG_OUT_SIZE_DT = float(sys.argv[3])

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

def pad_and_send(writer, s):
    l = int(MSG_OUT_SIZE + MSG_OUT_SIZE_DT * len(flags))
    if len(s) < l:
        s += " " + "A" * (l - len(s) - 1)
    s += "\n"
    writer.write(s.encode())

def accept_client(client_reader, client_writer):
    task = asyncio.Task(handle_client(client_reader, client_writer))

    def client_done(task):
        client_writer.close()

    task.add_done_callback(client_done)


@asyncio.coroutine
def handle_client(reader, writer):
    data = "+ I've got %d flags\n" % len(flags)
    writer.write(data.encode())

    while True:
        data = yield from reader.readline()
        if not data:
            break

        cmd, *args = [s.decode() for s in data.strip().split()]
        if cmd == "put":
            flag_id, flag = args[:2]
            flags[flag_id] = flag
            pad_and_send(writer, "+ ok")
        elif cmd == "get":
            flag_id = args[0]
            if flag_id not in flags:
                pad_and_send(writer, "- no such flag")
                continue
            pad_and_send(writer, "+ " + flags[flag_id])
        elif cmd == "check":
            flag_id, flag = args[:2]
            if flag_id not in flags:
                pad_and_send(writer, "- no such flag")
                continue

            if flag == flags[flag_id]:
                pad_and_send(writer, "+ ok")
            else:
                pad_and_send(writer, "- err")            
        elif cmd == "nop":
            pad_and_send(writer, "+ ok")
        elif cmd == "flags":
            out = " ".join(list(flags.values())[-100:])
            pad_and_send(writer, "+ " + out)
        else:
            pad_and_send(writer, "- wrong command")


def main():
    loop = asyncio.get_event_loop()
    f = asyncio.start_server(accept_client, host=None, port=PORT)
    loop.run_until_complete(f)
    loop.run_forever()

if __name__ == '__main__':
    main()
