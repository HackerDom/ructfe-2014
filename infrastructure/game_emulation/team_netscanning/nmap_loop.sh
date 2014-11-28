#!/bin/bash

while true; do
    timeout -s9 1800 /usr/bin/nmap -n -Pn --min-rate=256 --max-rate=256 --randomize-hosts 10.$((60 + RANDOM % 3)).0-255.0-192
done
