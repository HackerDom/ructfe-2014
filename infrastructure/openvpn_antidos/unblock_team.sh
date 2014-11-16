#!/bin/bash

if [ -z $1 ]; then
 echo "USAGE: block_team.sh team_num"
 exit
fi

if [[ ! $1 =~ ^[0-9]+$ ]]; then
 echo "Team num should be number"
 exit
fi

# add the couple of rules
iptables -t nat -D PREROUTING -m tcp -m comment --comment "antidos" -p tcp -i "tun${1}" -j DNAT --to-destination "10.60.${1}.1:10001"
