FROM ubuntu:trusty
MAINTAINER bay@hackerdom.ru

RUN apt-get update
RUN apt-get -y upgrade

ADD service.py /root/service.py

CMD ["/usr/bin/python3.4", "/root/service.py", "2000", "0", "0"]
