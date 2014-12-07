#!/bin/bash

# change directory to the script location
cd "$( dirname "${BASH_SOURCE[0]}")"

for name in team_s{1..8}; do
	docker build -t ructfe2014:${name} team_simpleservice
done
