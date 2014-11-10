#!/usr/bin/python
__author__ = 'm_messiah'

import socket

HOST = '0.0.0.0'
PORT = 27001
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setblocking(0)
s.bind((HOST, PORT))
s.listen(255)

while True:
    try:
        conn, addr = s.accept()
        print('Connected by', addr)
        data = conn.recv(256)
        conn.sendall(">> " + data)
        conn.close()
    except:
        pass