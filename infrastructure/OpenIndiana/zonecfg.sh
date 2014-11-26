#!/bin/bash

sed -i 's/PermitRootLogin no/PermitRootLogin yes/g' /etc/ssh/sshd_config
sed -i 's/CONSOLE=\/dev\/console/#CONSOLE=\/dev\/console/g' /etc/default/login
svcadm restart ssh:default
pkg install SUNWhea SUNWarc SUNWlibm SUNWlibms SUNWdfbh  SUNWlibC SUNWzlib gcc-43 wget gnu-make
