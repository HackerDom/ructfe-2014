#!/bin/bash

NETOPENED=$(cat /proc/sys/net/ipv4/ip_forward)

if [[ $NETOPENED == 1 ]]; then
  echo Network is opened

  for h in {0..255}; do
    iptables -t nat -w -C PREROUTING -i team${h} -p tcp -m tcp -m comment --comment closednetwork -j DNAT --to-destination 10.60.${h}.1:40002 &> /dev/null
    if [[ $? == 0 ]]; then
      echo "Warning: DNAT record still exists for team ${h}"
    fi
  done
   
else
  echo Network is closed

  for h in {0..255}; do
    iptables -t nat -w -C PREROUTING -i team${h} -p tcp -m tcp -m comment --comment closednetwork -j DNAT --to-destination 10.60.${h}.1:40002 &> /dev/null
    if [[ $? != 0 ]]; then
      echo "Warning: no DNAT record for team ${h}"
    fi
  done
fi
