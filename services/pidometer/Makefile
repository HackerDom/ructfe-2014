.PHONY: all network clean cython network-mac
CC=gcc

all: network server

server:
	$(CC) server.c -lsocket -lnsl

network: cython
	$(CC) -shared -O3 -Wall `python-config --cflags`  -c network.c -o network.so

network-mac: cython
	clang -fno-strict-aliasing -fno-common -dynamic -I/usr/local/include -I/usr/local/opt/sqlite/include -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -I/usr/local/Cellar/python/2.7.8_2/Frameworks/Python.framework/Versions/2.7/include/python2.7 -c network.c -o network.o
	clang -bundle -undefined dynamic_lookup -L/usr/local/lib -L/usr/local/opt/sqlite/lib network.o -o network.so
	rm -f network.o

clean:
	rm -f network.so
	rm -f *.pyc

cython:
	cython -D network.pyx
