#!/bin/bash

host_a="ructf-srv02g.ructf.yandex.net"
host_b="ructf-srv02h.ructf.yandex.net"

filename=$(date -u "+%Y%m%d-%H%M.txt.gz")

ssh_opts="-o StrictHostKeyChecking=no -o CheckHostIP=no"
ssh_opts="$ssh_opts -o NoHostAuthenticationForLocalhost=yes"
ssh_opts="$ssh_opts -o BatchMode=yes -o LogLevel=ERROR"
ssh_opts="$ssh_opts -o UserKnownHostsFile=/dev/null"

file_a="/var/checksystem_backup/a/${filename}"
file_b="/var/checksystem_backup/b/${filename}"

timeout -s9 180 ssh $ssh_opts "postgres@${host_a}" 'pg_dumpall | gzip' > $file_a
size=`stat -c %s $file_a`
if [[ $? != 0 || $size == 0 ]]; then
	ls -l $file_a |& mail -s "Site A backup failed!" bay@hackerdom.ru
fi

timeout -s9 180 ssh $ssh_opts "postgres@${host_b}" 'pg_dumpall | gzip' > $file_b
size=`stat -c %s $file_b`
if [[ $? != 0 || $size == 0 ]]; then
	ls -l $file_b |& mail -s "Site B backup failed!" bay@hackerdom.ru
fi
