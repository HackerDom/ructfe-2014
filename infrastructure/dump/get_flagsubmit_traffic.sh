#!/bin/bash

# A helper script to show realtime team data in wireshark
# Uses ssh connection to traffic dump server

filter="port 31337"
ssh root@ructf-srv02g.ructf.yandex.net "tcpdump -U -i eth0 -w - -s 0 ${filter}" | wireshark -k -i -
