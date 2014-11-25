#!/bin/bash
# adds rules for teams snat. Team will see incoming connections from 10.8{0..3}.{0..255}.1
# this script should be run once before the game starts

for num in {0..1023}; do 
    ip="10.$((80 + num / 256)).$((num % 256)).1"

    iptables -t nat -A POSTROUTING -o team${num} -j SNAT --to-source ${ip}
done
