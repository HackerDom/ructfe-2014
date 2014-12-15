#!/bin/bash

trap 'echo -e "\nYou can rerun this script by /root/first_setup.sh"; exit' INT

echo RuCTFe 2014 image setup
echo

if ! ifconfig -a | grep e1000g0 &>/dev/null; then
    echo "Warning: you don't have an e1000g0 interface. This can cause troubles."
    echo
fi

echo "Interface e1000g0 is your trunk uplink."
echo "Interface e1000g0 is preconfigured to use dhcp."
echo
echo "Interfaces e1000g0:1 e1000g0:2 are game interfaces"
echo
read -p "Let's configure network insterfaces. Enter your team number: " TEAM
echo

ipadd="10.$((60 + TEAM / 256)).$((TEAM % 256))."
services=(home vws dscheg pidometer glass)
for i in {1..4}
do
zonename=${services[$i]}
zonecfg -z $zonename <<EOF
select net physical=e1000g0
set address=${ipadd}$((i + 4))/24
end
verify
commit
exit
EOF

echo "Here is your $i service address:"
zonecfg -z $zonename info net
echo

zoneadm -z $zonename reboot
done

echo
echo "Network configuration is over"
echo
echo "Let's set your root password:"
passwd

echo
echo "That's all"
mv /root/first_setup.sh{,.bak}
