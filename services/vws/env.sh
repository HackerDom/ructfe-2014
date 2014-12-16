#!/bin/bash

pkgadd -d http://get.opencsw.org/now all
/opt/csw/bin/pkgutil -U -y
/opt/csw/bin/pkgutil -y -i gcc4core glib2 glib_dev libglib2_dev flex bison wget xz coreutils
pkg install gnu-coreutils gnu-tar SUNWhea SUNWarc SUNWlibm SUNWlibms SUNWdfbh  SUNWlibC SUNWzlib gettext libgee gnu-make gcc-43

export CPPFLAGS="-I/opt/csw/include"
export LDFLAGS="-L/opt/csw/lib -R/opt/csw/lib"
export PKG_CONFIG_PATH="/opt/csw/lib/pkgconfig"
export PATH="/opt/csw/bin:$PATH"

cd /root
wget --no-check-certificate http://ftp.gnome.org/pub/GNOME/sources/vala/0.26/vala-0.26.1.tar.xz
gtar --no-same-owner -xf vala-0.26.1.tar.xz
cd vala-0.26.1
./configure 
make

./compiler/valac -v --target-glib=2.0 --cc=/opt/csw/bin/gcc --vapidir=/root/vala-0.26.1/vapi --pkg gee-1.0 --pkg gio-2.0 -o /root/vws /root/vws.vala
mkdir /root/logs
rm -rf /root/vala-*
cat > /etc/init.d/vws <<EOF1
#!/bin/sh
case \$1 in
'start')
cd /root && LD_LIBRARY_PATH=/opt/csw/lib/ ./vws -p 2014 -i 20 -d stat/ -b 60 > logs/vws.log 2> logs/vws.err &
;;
'stop')
kill \`/usr/bin/head -n 1 /root/logs/vws.err\`
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

echo "if OK, then remove sources"
# reboot
