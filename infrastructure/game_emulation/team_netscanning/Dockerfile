FROM ubuntu:trusty
MAINTAINER bay@hackerdom.ru

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install nmap

ADD nmap_loop.sh /root/

CMD ["/root/nmap_loop.sh"]
