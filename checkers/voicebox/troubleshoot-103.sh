#!/bin/bash
cat micro.checksystem.err*log | grep ^103 -B10 | sed -e "s/.*msg: //" | sed -e "s/.*idea //"

