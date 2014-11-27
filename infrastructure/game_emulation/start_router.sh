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

cid=$(docker run --privileged --name ${full_name} --memory=2048m --cpu-shares=10 -d ructfe2014:${name} /usr/sbin/openvpn /etc/openvpn/${team_num}.conf)

ip="10.$((60 + team_num / 256)).$((team_num % 256)).1/24"

# add eth1 interface
pipework/pipework br$((team_num + 10000)) ${cid} ${ip}
