#!/bin/bash

while true; do
    timeout -s9 1800 /usr/bin/nmap -n -p1-65535 -Pn --min-rate=384 --max-rate=384 --randomize-hosts 10.$((60 + RANDOM % 3)).$((RANDOM % 256)).0-192
done
