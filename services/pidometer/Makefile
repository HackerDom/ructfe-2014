.PHONY: server server-mac clean
CC=gcc

server-mac:
	$(CC) server.c `python-config --cflags` `python-config --ldflags` -o Server

server:
	$(CC) server.c -lsocket -lnsl `python-config --cflags` `python-config --ldflags` -o Server

clean:
	rm Server
	rm -f *.pyc