#!/bin/bash

name=team_netscanning

# change directory to the script location
cd "$( dirname "${BASH_SOURCE[0]}")"

docker build -t ructfe2014:${name} ${name}
