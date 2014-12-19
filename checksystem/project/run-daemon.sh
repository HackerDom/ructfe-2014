#!/bin/bash
if [ -z "$1" ]
then
	echo "Give checkers.cfg as argument"
	exit 1
fi

java -classpath .:external/postgresql-9.3-1102.jdbc41.jar:external/junit-4.6.jar:external/log4j-1.2.17.jar ructf.daemon.Main daemon.cfg $1
