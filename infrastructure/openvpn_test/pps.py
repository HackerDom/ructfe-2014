#!/usr/bin/python

import os
import time

ifaces = os.listdir("/sys/class/net/")

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

for iface in ifaces:
	print("TX %s: %d pkts/10s RX %s: %d pkts/10s" % (
		iface, get_tx(iface) - pkts_out[iface], iface, 
		get_rx(iface) - pkts_in[iface]))
