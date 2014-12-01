#!/bin/bash

team_num=${1?Usage: ./stop_router.sh <team_num>}

name=team_router
full_name=${name}_${team_num}

docker stop ${full_name}
docker rm ${full_name} &>/dev/null
