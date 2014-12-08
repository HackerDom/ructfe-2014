#!/bin/bash

team_num=${1?Usage: ./stop_s1.sh <team_num>}

name=team_s1
full_name=${name}_${team_num}

docker stop ${full_name}
docker rm ${full_name} &>/dev/null
