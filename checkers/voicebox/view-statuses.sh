#!/bin/bash
grep "^[0-9][0-9][0-9]:" micro.checksystem.err.log  | cut -d : -f 1 | sort | uniq -c
