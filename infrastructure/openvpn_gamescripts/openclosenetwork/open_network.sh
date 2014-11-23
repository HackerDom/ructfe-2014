#!/bin/bash

# go to script dir
cd "$( dirname "${BASH_SOURCE[0]}" )"

echo 1 > /proc/sys/net/ipv4/ip_forward

for h in {0..255}; do
    while iptables -t nat -C PREROUTING -i team${h} -p tcp -m tcp -m comment --comment closednetwork -j DNAT --to-destination 10.60.${h}.1:40002 &>/dev/null; do
        iptables -t nat -D PREROUTING -i team${h} -p tcp -m tcp -m comment --comment closednetwork -j DNAT --to-destination 10.60.${h}.1:40002
    done;
done

./check_network.sh