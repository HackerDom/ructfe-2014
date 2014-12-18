#!/bin/bash

pkgadd -d http://get.opencsw.org/now all
/opt/csw/bin/pkgutil -U -y
pkg install SUNWhea SUNWarc SUNWlibm SUNWlibms SUNWdfbh  SUNWlibC SUNWzlib gcc-43 gnu-make SUNWpython26-setuptools netcat
/opt/csw/bin/pkgutil -y -i libmcrypt4 mcrypt_dev redis
ln -sf /usr/gcc/4.3/bin/gcc /usr/bin/gcc

echo "export CPPFLAGS=\"-I/opt/csw/include\"" >> /root/.profile
echo "export LDFLAGS=\"-L/opt/csw/lib -R/opt/csw/lib\"" >> /root/.profile
echo "export PKG_CONFIG_PATH=\"/opt/csw/lib/pkgconfig\"" >> /root/.profile
source /root/.profile

easy_install redis python-mcrypt

cat > /etc/redis.conf <<EOF
daemonize yes
port 6379
logfile /opt/redis.log
pidfile /opt/redis.pid
save 900 5
save 300 2
save 60  1
dbfilename db.rdb
dir /opt/
# rename-command CONFIG ""
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

cat > /etc/init.d/pidometer <<EOF2
#!/bin/sh
case \$1 in
'start')
PYTHONPATH=/root/pidometer/ /root/pidometer/Server >/root/pidometer/server.log 2> /opt/pidometer.pid &
;;
'stop')
kill \`/usr/bin/head -n 1 /opt/pidometer.pid\`
;;
*)
echo "Usage: \$0 start|stop" >&2
exit 1
;;
esac
exit 0
EOF2
chmod +x /etc/init.d/pidometer
ln -sf /etc/init.d/pidometer /etc/rc3.d/S30pidometer

cd /root/pidometer && make server

# reboot
