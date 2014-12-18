#!/bin/bash

pkgadd -d http://get.opencsw.org/now all
/opt/csw/bin/pkgutil -U -y
pkg install wget
/opt/csw/bin/pkgutil -y -i libstdc++6 redis
wget http://download.mono-project.com/third-party/codice/2.10/mono-2.10-sgen-opensolaris-x86.pkg.gz
gunzip mono-2.10-sgen-opensolaris-x86.pkg.gz
pkgadd -d mono-2.10-sgen-opensolaris-x86.pkg all

cat > /etc/redis.conf <<EOF
daemonize yes
bind 127.0.0.1
port 6379
logfile /opt/redis.log
pidfile /opt/redis.pid
save 900 1
save 300 5
save 60  10
dbfilename db.rdb
dir /opt/
EOF

cat > /etc/init.d/redis <<EOF1
#!/bin/sh
case \$1 in
'start')
/opt/csw/bin/redis-server /etc/redis.conf
;;
'stop')
kill \`/usr/bin/cat /opt/redis.pid\`
;;
*)
echo "Usage: \$0 start|stop" >&2
exit 1
;;
esac
exit 0
EOF1
chmod +x /etc/init.d/redis
ln -sf /etc/init.d/redis /etc/rc3.d/S20redis

cat > /etc/init.d/heart <<EOF2
#!/bin/sh
case \$1 in
'start')
cd /root/heart && LD_LIBRARY_PATH=/opt/csw/lib /opt/mono/bin/mono heart.exe 127.0.0.1:6379 &
;;
'stop')
echo "Use ps aux | grep heart and kill <PID>"
;;
*)
echo "Usage: \$0 start|stop" >&2
exit 1
;;
esac
exit 0
EOF2
chmod +x /etc/init.d/heart
ln -sf /etc/init.d/heart /etc/rc3.d/S30heart


echo "Complete"

# reboot

