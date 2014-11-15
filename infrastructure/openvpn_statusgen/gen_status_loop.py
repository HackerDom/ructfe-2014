#!/usr/bin/python3

import jinja2
import subprocess
import re
import time
import traceback
import os

from teams import teams

ROUTER_PINGONCE_FILE = "router_ping_once.txt"
IMAGE_PINGONCE_FILE = "image_ping_once.txt"

TEMPLATE_FILE = "status.tpl"
STATUS_HTML = "/usr/share/nginx/html/HBcUe2F2/status.html"

PAUSE = 1

ROUTER_IP = "10.60.N.2"
IMAGE_IP = "10.70.N.100"


def get_hosts_ping(hosts):
    """ returns: host -> ping_time | None """
    fping_base = ["fping", "-q", "-C1", "-t5000"]

    ret = {}

    router_ping_proc = subprocess.Popen(fping_base + hosts,
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
                print("Surprising output: %s" % err.decode())

    return ret


def loop():
    # create flags files if not exists
    open(ROUTER_PINGONCE_FILE, 'ab').close()
    open(IMAGE_PINGONCE_FILE,  'ab').close()

    routers_pingonce_data = open(ROUTER_PINGONCE_FILE, "r", 1).read()
    images_pingonce_data = open(IMAGE_PINGONCE_FILE, "r", 1).read()

    routers_pingonce = set(re.findall(r"\d+", routers_pingonce_data))
    images_pingonce = set(re.findall(r"\d+", images_pingonce_data))

    # get list to ping
    team_to_router = {}
    team_to_image = {}

    router_to_team = {}
    image_to_team = {}

    for team in teams:
        team_router = ROUTER_IP.replace("N", str(team))
        team_image = IMAGE_IP.replace("N", str(team))

        team_to_router[team] = team_router
        team_to_image[team] = team_image

        router_to_team[team_router] = team
        image_to_team[team_image] = team

    # ping teams
    router_pings = get_hosts_ping(list(team_to_router.values()))
    image_pings = get_hosts_ping(list(team_to_image.values()))

    # generate result dict for each team
    result = []
    for team in teams:
        team_name = teams[team]
        team_router = team_to_router[team]
        team_image = team_to_image[team]

        router_ping = router_pings.get(team_router)
        router_pingonce = str(team) in routers_pingonce
        image_ping = image_pings.get(team_router)
        image_pingonce = str(team) in images_pingonce

        print(image_pingonce, images_pingonce)

        if router_ping is not None:
            if str(team) not in routers_pingonce:
                router_pingonce = True
                routers_pingonce.add(str(team))

                with open(ROUTER_PINGONCE_FILE, "a") as f:
                    f.write(str(team) + "\n")

        if image_ping is not None:
            if str(team) not in images_pingonce:
                image_pingonce = True
                images_pingonce.add(str(team))

                with open(IMAGE_PINGONCE_FILE, "a") as f:
                    f.write(str(team) + "\n")

        result.append({"id": team,
                       "name": team_name,
                       "router_ping": router_ping,
                       "router_pingonce": router_pingonce,
                       "image_ping": image_ping,
                       "image_pingonce": image_pingonce})

    # generate html by result
    template = open(TEMPLATE_FILE).read()
    html = jinja2.Template(template).render(result=result)
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
