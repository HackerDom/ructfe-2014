#!/bin/bash

# A helper script to show realtime team data in wireshark
# Uses ssh connection to traffic dump server

filter="$1"

if [ -z $filter ]; then
 echo "USAGE: ./traffic.sh <tcpdump rule>"
 echo "Do not forget to filter out the ssh traffic"
 exit
fi

ssh root@ructf-srv06g.ructf.yandex.net "tcpdump -U -i eth0 -w - -s 0 ${filter}" | wireshark -k -i -
