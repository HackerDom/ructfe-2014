#!/bin/bash

pkg install SUNWhea SUNWarc SUNWlibm SUNWlibms SUNWdfbh  SUNWlibC SUNWzlib gcc-43 gnu-make flex bison wget gettext xz
ln -sf /usr/gcc/4.3/bin/gcc /usr/bin/gcc

cd /root
wget http://ftp.gnome.org/pub/GNOME/sources/vala/0.26/vala-0.26.1.tar.xz
tar xf vala-0.26.1.tar.xz
cd vala-0.26.1
./configure --prefix=/usr/
make install

cat > /etc/init.d/vws <<EOF1
#!/bin/sh
case \$1 in
'start')
cd /export/vws && ./vws -p 2014 -i 20 -d stat/ >logs/vws.log 2>logs/vws.err &
;;
'stop')
kill \`/usr/bin/head -n 1 /export/vws/vws.err\`
;;
*)
echo "Usage: \$0 start|stop" >&2
exit 1
;;
esac
exit 0
EOF1
chmod +x /etc/init.d/vws
ln -sf /etc/init.d/vws /etc/rc3.d/S20vws

# reboot
