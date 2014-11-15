#!/usr/bin/python3.4

import random
import asyncio
import sys
import signal
import time

TIMEOUT = 7


def genstring(n):
    abc = list("1234567890abcdef")
    ret = []
    for i in range(n):
        ret.append(random.choice(abc))
    return "".join(ret)


@asyncio.coroutine
def handle_client(host, port):
    start_time = time.time()

    try:
        reader, writer = yield from asyncio.open_connection(host, port)
    except:
        return

    try:
        flag_id = genstring(6)
        flag = genstring(32) + "="

        writer.write(("put %s %s\n" % (flag_id, flag)).encode())
        data = yield from asyncio.wait_for(reader.readline(), TIMEOUT)
        if data != b"+ ok\n":
            return

        writer.write(("check %s %s\n" % (flag_id, flag)).encode())
        data = yield from asyncio.wait_for(reader.readline(), TIMEOUT)
        if data != b"+ ok\n":
            return

        writer.write(("check %s %s\n" % (flag_id, flag[:-1])).encode())
        data = yield from asyncio.wait_for(reader.readline(), TIMEOUT)
        if data != b"- err\n":
            return

        writer.write(("check %s %s\n" % (flag_id, flag)).encode())
        data = yield from asyncio.wait_for(reader.readline(), TIMEOUT)
        if data != b"+ ok\n":
            return

        end_time = time.time()
        sys.stderr.write("%s : %.02g\n" % (host, end_time - start_time))
    finally:
        writer.close()


def main():
    loop = asyncio.get_event_loop()

    tasks = [asyncio.Task(handle_client(ip, 31337)) for ip in sys.argv[1:]]
    loop.run_until_complete(asyncio.wait(tasks))

if __name__ == '__main__':
    signal.alarm(TIMEOUT)
    main()
