#!/usr/bin/python2

base = """ 
mode p2p
dev tun
remote tesla41 %d
secret static.key
ifconfig 10.100.%d.2 10.100.%d.1
#route 10.100.0.0 255.255.0.0
%s
ping 10
ping-restart 30
nobind
verb 3"

"""

for i in range(256):
    phys_num = i % 12
    
    cur_routes = []
    for j in range(256):
        other_phys_num = j % 12
        
        if phys_num == other_phys_num:
            continue
        
        cur_routes.append("route" )
        
    
    open("client_conf_%d.conf" % i, "w").write(base % (30000 + i, i, i))
