#!/usr/bin/python2

import random

base = """ 
mode p2p
dev tun
remote tesla41 %d
secret static.key
ifconfig 10.100.%d.2 10.100.%d.1
%s
ping 10
ping-restart 30
nobind
verb 3"

"""

HOSTS = ["tesla31", "tesla32", "tesla33", "tesla34", 
         "tesla35", "tesla36", "tesla37", "tesla38",
         "tesla39", "tesla42", "tesla43", "tesla44"
         ]

CONFIGS_NUM = 252

assert CONFIGS_NUM % len(HOSTS) == 0  # don't want to think ^)

physhost_net_loghost_map = {} # physhostnum -> net_num -> loghost_num

for phys_num in range(len(HOSTS)):
    physhost_net_loghost_map[phys_num] = {}

for phys_num in range(len(HOSTS)):
    nums_with_this_host = list(range(phys_num, CONFIGS_NUM, len(HOSTS)))
 
    for remote_host in range(len(HOSTS)):
        if remote_host == phys_num:
            continue

        nums_with_this_remote_host = list(range(remote_host, CONFIGS_NUM, len(HOSTS)))
        
        random.shuffle(nums_with_this_host)

        for pos, i in enumerate(nums_with_this_remote_host):
            if i in physhost_net_loghost_map[phys_num]:
                continue

            chosen_num = nums_with_this_host[pos]

            physhost_net_loghost_map[phys_num][i] = chosen_num
            physhost_net_loghost_map[remote_host][chosen_num] = i
        

print(physhost_net_loghost_map)
for phys_num in physhost_net_loghost_map:
    assert len(physhost_net_loghost_map[phys_num]) + len(list(range(phys_num, CONFIGS_NUM, len(HOSTS)))) == CONFIGS_NUM

for num in range(CONFIGS_NUM):
    phys_num = num % len(HOSTS)
    
    routes = []
    for net_num in physhost_net_loghost_map[phys_num]:
        log_num = physhost_net_loghost_map[phys_num][net_num]

        if log_num == num: 
            routes.append("route 10.100.%d.0 255.255.255.252" % net_num)

    open("client_conf_%s_%d.conf" % (HOSTS[phys_num], num), "w").write(base % (30000 + num, num, num, "\n".join(routes)))
