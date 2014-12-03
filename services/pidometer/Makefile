.PHONY: all network clean cython
CC=gcc

all: network server
	rm -rf build

server:
	$(CC) server.c -lsocket -lnsl

network: cython
	$(CC) -shared -dynamic -O3 -Wall `python-config --cflags`  -c network.c -o libnetwork.so

clean:
	rm -f libnetwork.so
	rm -f *.pyc

cython:
	cython -D network.pyx
