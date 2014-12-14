FROM ubuntu:trusty
MAINTAINER bay@hackerdom.ru

RUN apt-get update
RUN apt-get -y upgrade

ADD exploit_farm /root/

CMD ["/root/exploit_farm/start.sh"]
