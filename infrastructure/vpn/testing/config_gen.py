#!/usr/bin/python2

base = """ 
mode p2p
port %d

dev tun%d
ifconfig 10.100.%d.1 10.100.%d.2
secret static.key
#keepalive 10 60
ping 10
ping-restart 60
ping-timer-rem
persist-tun
persist-key
"""

for i in range(256):
	open("conf_%d.conf" % i, "w").write(base % (30000 + i, i, i, i))
