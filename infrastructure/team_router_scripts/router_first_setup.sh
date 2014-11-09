#!/bin/bash

trap 'echo -e "\nYou can rerun this script by /root/router_first_setup.sh"; exit' INT

echo RuCTFe 2014 Router Setup
echo

if ! ip link show eth0 &>/dev/null; then
 echo "Warning: you don't have an eth0 interface. This can cause troubles."
 echo
fi

if ! ip link show eth1 &>/dev/null; then
 echo "Warning: you don't have an eth1 interface. This can cause troubles."
 echo
fi

echo "Interface eth0 is your uplink, eth1 - is an internal interface"
read -p "Lets generate eth1 config. Enter your team number: " TEAM

echo "auto eth1" > /etc/network/interfaces.d/eth1.cfg
echo "iface eth1 inet static" >> /etc/network/interfaces.d/eth1.cfg
echo "address 10.70.${TEAM}.1" >>  /etc/network/interfaces.d/eth1.cfg
echo "netmask 255.255.255.0" >>  /etc/network/interfaces.d/eth1.cfg

echo "Here is your new /etc/network/interfaces.d/eth1.cfg:"
cat /etc/network/interfaces.d/eth1.cfg
echo

ifup eth1

echo -n "Lets generate eth0 config. "
read -p "Press enter to execute nano /etc/network/interfaces.d/eth0.cfg..."
nano /etc/network/interfaces.d/eth0.cfg

ifup eth0

echo
echo "Network configuration is over"
echo
read -p "Press enter to generate root password and to start ssh..."

PASS=$(pwgen -Bs 8 1)
chpasswd <<< "root:${PASS}"
echo "Your new root password is ${PASS}"

/etc/init.d/ssh start

echo
echo "Further steps:"
echo "- copy your vpn config to /etc/openvpn/*.conf"
echo "- start the vpn with /etc/init.d/openvpn start"
echo
echo "Yep, that's all"
