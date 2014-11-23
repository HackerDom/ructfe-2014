#!/bin/bash
# removes rules for teams snat
# this script shouldn't be run normally :)

for h in {0..255}; do 
    iptables -t nat -D POSTROUTING -o team${h} -j SNAT --to-source 10.60.${h}.1
done
