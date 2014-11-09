import os
import sys

N = 64

SERVER = "178.62.129.38"

CLIENT_DATA = """mode p2p
dev tun
remote {0} {1}
ifconfig 10.60.{2}.2 10.60.{2}.1
route 10.60.0.0 255.255.0.0
route 10.70.0.0 255.255.0.0
keepalive 10 30
nobind
verb 3

tun-mtu 1500
fragment 1300
mssfix

<secret>
{3}
</secret>
"""

if __name__ != "__main__":
    print("I am not a module")
    sys.exit(0)

# gen client configs
os.chdir(os.path.dirname(os.path.realpath(__file__)))
try:
    os.mkdir("client")
except FileExistsError:
    print("Remove ./client dir first")
    sys.exit(1)

for i in range(N):
    key = open("keys/%d.key" % i).read()

    data = CLIENT_DATA.format(SERVER, 30000+i, i, key)
    open("client/%d.conf" % i, "w").write(data)

print("Finished, check ./client dir")
    