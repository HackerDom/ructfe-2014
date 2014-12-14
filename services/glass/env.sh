#!/bin/bash

pkgadd -d http://get.opencsw.org/now
/opt/csw/bin/pkgutil -U
/opt/csw/bin/pkgutil -i -y python33 nginx wget

sed -i '/server/,$d' /etc/opt/csw/nginx/nginx.conf
cat >> /etc/opt/csw/nginx/nginx.conf <<EOF1
    server {
        listen 8000;
        access_log  /root/glass/nginx.log;
    
        location / {
            proxy_pass http://127.0.0.1:8001;
            proxy_set_header Host \$server_name;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        }
    }
}
EOF1
ln -s /etc/opt/csw/init.d/cswnginx /etc/rc3.d/S20nginx

/opt/csw/bin/wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
/opt/csw/bin/python3 get-pip.py
/opt/csw/bin/pip3 install gunicorn
# gunicorn wsgi:application --bind 0.0.0.0:8001 &> gunicorn.log

cat > /etc/init.d/glass <<EOF
#!/bin/sh
case \$1 in
'start')
cd /root/glass/ && /opt/csw/bin/gunicorn wsgi:application --bind 0.0.0.0:8001 > gunicorn.log 2>&1 &
;;
'stop')
kill \`/usr/bin/cat /var/run/glass.pid\`
;;
*)
echo "Usage: \$0 start|stop" >&2
exit 1
;;
esac
exit 0
EOF
chmod +x /etc/init.d/glass
ln -s /etc/init.d/glass /etc/rc3.d/S20glass
