#!/bin/bash

while true; do
 ip=10.100.$((RANDOM % 252)).2
 # make 1000 connections on random ip
 ab -c 2 -n 1000 http://$ip/1mb.dat
 sleep 10
done
