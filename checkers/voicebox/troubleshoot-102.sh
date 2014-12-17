#!/bin/bash
cat micro.checksystem.err*log | grep ^102 -B2 | sed -e "s/.*msg: //" | sed -e "s/.*idea //"

