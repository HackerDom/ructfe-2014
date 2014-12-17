#!/bin/bash

trap 'echo -e "\nYou can rerun this script by /root/first_setup.sh"; exit' INT

echo RuCTFe 2014 image setup
echo

echo "Let's set your root password:"
passwd

if ! ifconfig -a | grep e1000g0 &>/dev/null; then
    echo "Warning: you don't have an e1000g0 interface. This can cause troubles."
    echo

fi

echo "Interface e1000g0 is your trunk uplink."
echo
read -p "Let's configure network insterfaces. Enter your team number: " TEAM
echo

ipadd="10.$((60 + TEAM / 256)).$((TEAM % 256))."
ipadm delete-addr e1000g0/v4static
ipadm create-addr -T static -a ${ipadd}10/24 e1000g0/v4static
route flush
route -p flush
route -p add default ${ipadd}1
svcadm restart svc:/network/physical:default

services=(home vws heart pidometer glasses)
for i in {1..4}
do
zonename=${services[$i]}

cp /etc/shadow /export/$zonename/root/etc/shadow

zonecfg -z $zonename <<EOF
select net physical=e1000g0
set address=${ipadd}$((i + 4))/24
set defrouter=${ipadd}1
end
verify
commit
exit
EOF

echo
echo "$i service has ${ipadd}$((i + 4)) ipaddr"
echo "Rebooting $i zone... Please wait..."
zoneadm -z $zonename reboot
done

echo
echo "Network configuration is over"
echo "You can connect to this host by ssh root@${ipadd}10"

echo
echo "That's all. Please rename /root/first_setup.sh for safety"
echo
#mv /root/first_setup.sh{,.bak}
