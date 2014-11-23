#!/bin/bash
# adds rules for teams snat. Team will see incoming connections from 10.60.N.1
# this script should be run once before the game starts

for h in {0..255}; do 
    if ! iptables -t nat -C POSTROUTING -o team${h} -j SNAT --to-source 10.60.${h}.1; then
        echo "Holy sheet! Team ${h} is not SNATted!!!"
        echo "You can fix it with this command"
        echo "iptables -t nat -A POSTROUTING -o team${h} -j SNAT --to-source 10.60.${h}.1"
    fi
done
