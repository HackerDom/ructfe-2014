#!/bin/bash
cat micro.checksystem.err*log | grep "^[0-9][0-9][0-9]:" | cut -d : -f 1 | sort | uniq -c
