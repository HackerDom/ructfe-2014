#!/usr/bin/python

import os
import time

ifaces = os.listdir("/sys/class/net/")

ifaces = [iface for iface in ifaces if iface.startswith("tun")]

pkts_in = {}
pkts_out = {}

def get_rx(iface):
	return int(open("/sys/class/net/%s/statistics/rx_packets" % iface).read())

def get_tx(iface):
	return int(open("/sys/class/net/%s/statistics/tx_packets" % iface).read())


for iface in ifaces:
	pkts_in[iface] = get_rx(iface)
	pkts_out[iface] = get_tx(iface)

time.sleep(10)

tx = 0
rx = 0

for iface in ifaces:
    tx += get_tx(iface) - pkts_out[iface]
    rx += get_rx(iface) - pkts_in[iface]

print("TX: %s pkt/sec RX: %s pkt/sec" % (tx // 10, rx // 10))
