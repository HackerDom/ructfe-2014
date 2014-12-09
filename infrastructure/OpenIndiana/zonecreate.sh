#!/bin/bash

#zonename=$1
zonename="khozov"
#ipaddr=$2
ipaddr=8
mkdir /export/$zonepath
chown root:root /export/$zonepath
chmod 700 /export/$zonepath

zonecfg -z $zonename << EOF
    create -b
    set zonepath=/export/$zonename
    set autoboot=true
    add net
      set physical=xnf0
      set address=172.16.16.$ipaddr/24
      end
    verify
    commit
    exit
EOF

zoneadm -z $zonename install
zoneadm -z $zonename boot
zlogin -C $zonename
