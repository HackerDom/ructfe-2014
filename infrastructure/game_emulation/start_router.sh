#!/bin/bash

# change directory to the script location
cd "$( dirname "${BASH_SOURCE[0]}")"

team_num=${1?Usage: ./start.router.sh <team_num>}

name=team_router
full_name=${name}_${team_num}

if docker stop ${full_name} &>/dev/null; then
    echo "Deleting old container, hope you knew it :)"
    docker rm ${full_name}
fi

cid=$(docker run --net=none --privileged --name ${full_name} --memory=2048m --cpu-shares=10 -d ructfe2014:${name} /usr/sbin/openvpn /etc/openvpn/${team_num}.conf)

ip="10.$((60 + team_num / 256)).$((team_num % 256)).1/24"
bridged_ip="10.$((100 + team_num / 256)).$((team_num % 256)).2/24"
bridged_router="10.$((100 + team_num / 256)).$((team_num % 256)).1"

# add eth1 interface
pipework/pipework br$((team_num + 10000)) ${cid} ${ip}

# set eth0 interface
pipework/pipework br$((team_num + 20000)) -i eth0 ${cid} ${bridged_ip}@${bridged_router}
ip addr add ${bridged_router}/24 dev br$((team_num + 20000))

if ! iptables -t nat -C POSTROUTING -o eth0 -j MASQUERADE &>/dev/null; then
 echo "Autoexecuting: iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE"
 echo "If you don't need it, comment it"
 iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
fi

# do not forget do iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE on the host computer