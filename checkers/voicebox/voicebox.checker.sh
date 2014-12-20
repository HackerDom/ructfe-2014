#!/bin/bash
java -Dmbrola.base=checker/mbrola -cp "freeTTS/freetts-1.2/lib/freetts.jar:checker/out/production/checker:jdbc/postgresql-9.3-1102.jdbc41.jar" Checker "$@"

