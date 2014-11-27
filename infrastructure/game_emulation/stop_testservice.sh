#!/bin/bash

team_num=${1?Usage: ./stop_testservice.sh <team_num>}

name=team_testservice
full_name=${name}_${team_num}

docker stop ${full_name}
docker rm ${full_name} &>/dev/null
