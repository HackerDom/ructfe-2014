#!/bin/bash

trap 'echo -e "\nYou can rerun this script by /root/testimage_first_setup.sh"; exit' INT

echo RuCTFe 2014 Test Image Setup
echo

if ! ip link show eth0 &>/dev/null; then
 echo "Warning: you don't have an eth0 interface. This can cause troubles."
 echo
fi

read -p "Lets generate eth0 config. Enter your team number: " TEAM

echo "auto eth0" > /etc/network/interfaces.d/eth0.cfg
echo "iface eth0 inet static" >> /etc/network/interfaces.d/eth0.cfg
echo "address 10.70.${TEAM}.100" >>  /etc/network/interfaces.d/eth0.cfg
echo "netmask 255.255.255.0" >>  /etc/network/interfaces.d/eth0.cfg
echo "gateway 10.70.${TEAM}.1" >>  /etc/network/interfaces.d/eth0.cfg

echo "Here is your new /etc/network/interfaces.d/eth0.cfg:"
cat /etc/network/interfaces.d/eth0.cfg
echo

ifup eth0

echo
echo "Network configuration is over"
echo
