FROM ubuntu:trusty
MAINTAINER bay@hackerdom.ru

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install openvpn

ADD vpn.tar.gz /etc/openvpn

CMD ["/usr/sbin/openvpn"]
