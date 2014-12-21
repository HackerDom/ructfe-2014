#!/usr/bin/python3

import jinja2
import subprocess
import re
import time
import traceback
import os

from teams import get_teams

TEMPLATE_FILE = "status.tpl"
STATUS_HTML = "status.html"

PAUSE = 1

def get_image_ip(team):
    return "10.%s.%s.100" % (60 + team // 256, team % 256)

def get_ip3oct(team):
    return "10.%s.%s." % (60 + team // 256, team % 256)



def get_ping_like_cmd_parsed_ret(args, hosts):
    ret = {}

    router_ping_proc = subprocess.Popen(args + hosts,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
    out, err = router_ping_proc.communicate()
    # print(out)
    for line in err.decode().split("\n"):
        if ":" not in line:
            continue
        host, result = map(str.strip, line.split(":", 1))

        if host not in hosts:
            continue

        try:
            ret[host] = float(result)
        except ValueError:
            if result == "-":
                ret[host] = None
            else:
                print("Surprising output: %s" % line)

    return ret


def is_net_opened():
    return open("/proc/sys/net/ipv4/ip_forward").read()[0] == "1"

def get_hosts_ping(hosts):
    """ returns: host -> ping_time | None """
    fping_base = ["fping", "-q", "-C1", "-t1000"]
    return get_ping_like_cmd_parsed_ret(fping_base, hosts)


def loop():
    teams = get_teams()

    # create flags files if not exists

    # get list to ping
    team_to_image = {}
    team_to_s1 = {}
    team_to_s2 = {}
    team_to_s3 = {}
    team_to_s4 = {}
    team_to_s5 = {}
    team_to_s6 = {}
    team_to_s7 = {}
    team_to_s8 = {}

    for team in teams:
        team_image = get_image_ip(team)
        team_s3oct = get_ip3oct(team)

        team_to_image[team] = team_image
        team_to_s1[team] = team_s3oct + "1"
        team_to_s2[team] = team_s3oct + "2"
        team_to_s3[team] = team_s3oct + "3"
        team_to_s4[team] = team_s3oct + "4"
        team_to_s5[team] = team_s3oct + "5"
        team_to_s6[team] = team_s3oct + "6"
        team_to_s7[team] = team_s3oct + "7"
        team_to_s8[team] = team_s3oct + "8"


    # ping teams
    image_pings = get_hosts_ping(list(team_to_image.values()))

    s1_pings = get_hosts_ping(list(team_to_s1.values()))
    s2_pings = get_hosts_ping(list(team_to_s2.values()))
    s3_pings = get_hosts_ping(list(team_to_s3.values()))
    s4_pings = get_hosts_ping(list(team_to_s4.values()))
    s5_pings = get_hosts_ping(list(team_to_s5.values()))
    s6_pings = get_hosts_ping(list(team_to_s6.values()))
    s7_pings = get_hosts_ping(list(team_to_s7.values()))
    s8_pings = get_hosts_ping(list(team_to_s8.values()))


    # generate result dict for each team
    result = []
    for team in teams:
        team_name = teams[team]
        team_image = team_to_image[team]

        team_s1 = team_to_s1[team]
        team_s2 = team_to_s2[team]
        team_s3 = team_to_s3[team]
        team_s4 = team_to_s4[team]
        team_s5 = team_to_s5[team]
        team_s6 = team_to_s6[team]
        team_s7 = team_to_s7[team]
        team_s8 = team_to_s8[team]

        image_ping = image_pings.get(team_image)
        
        s1_ping = s1_pings.get(team_s1)
        s2_ping = s2_pings.get(team_s2)
        s3_ping = s3_pings.get(team_s3)
        s4_ping = s4_pings.get(team_s4)
        s5_ping = s5_pings.get(team_s5)
        s6_ping = s6_pings.get(team_s6)
        s7_ping = s7_pings.get(team_s7)
        s8_ping = s8_pings.get(team_s8)

        result.append({"id": team,
                       "name": team_name,
                       "image_ip": team_to_image[team],
                       "s1_ip": team_s1,
                       "s2_ip": team_s2,
                       "s3_ip": team_s3,
                       "s4_ip": team_s4,
                       "s5_ip": team_s5,
                       "s6_ip": team_s6,
                       "s7_ip": team_s7,
                       "s8_ip": team_s8,
                       "image_ping": image_ping,
                       "s1_ping": s1_ping,
                       "s2_ping": s2_ping,
                       "s3_ping": s3_ping,
                       "s4_ping": s4_ping,
                       "s5_ping": s5_ping,
                       "s6_ping": s6_ping,
                       "s7_ping": s7_ping,
                       "s8_ping": s8_ping,
                       })

    # compute sums
    sums = {}

    for col in ("image_ping",
                "s1_ping", "s2_ping", "s3_ping", 
                "s4_ping", "s5_ping", "s6_ping", "s7_ping", "s8_ping"):
        sums[col] = sum(bool(row[col]) for row in result)
    print(sums)


    # generate html by result
    template = open(TEMPLATE_FILE, encoding="utf8").read()
    time_str = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
    html = jinja2.Template(template, autoescape=True).render(
        result=result, time=time_str, netopened=is_net_opened(), sums=sums)
    open(STATUS_HTML, "w").write(html)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    while True:
        try:
            loop()
        except:
            traceback.print_exc()
        finally:
            print("Sleeping %d" % PAUSE)
            time.sleep(PAUSE)
