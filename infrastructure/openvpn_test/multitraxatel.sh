#!/bin/bash

# go to script directory
cd "$( dirname "${BASH_SOURCE[0]}" )"

for i in {0..63}; do
 ./traxatel.sh &
done