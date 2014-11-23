#!/bin/bash
# adds rules for teams snat. Team will see incoming connections from 10.60.N.1
# this script should be run once before the game starts

for h in {0..255}; do 
    iptables -t nat -A POSTROUTING -o team${h} -j SNAT --to-source 10.60.${h}.1
done
