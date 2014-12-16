#!/bin/bash
grep ^102 -B2 micro.checksystem.err.log | sed -e "s/.*msg: //" | sed -e "s/.*idea //"

