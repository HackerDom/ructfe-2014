#!/bin/bash
clear="rm -f /root/.bash_history /var/adm/* /var/log/* /var/logadm/* && history -c"

for zone in vws heart pidometer glasses
do
    echo "Clearing $zone"
    zlogin $zone eval $clear
done

echo "Clearing GLOBAL"
eval $clear