.PHONY: all cutils network clean cython

all: cutils network
	rm -rf build

cutils:
	clang -fno-strict-aliasing -fno-common -dynamic -I/usr/local/include -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -I/usr/local/Cellar/python/2.7.8_2/Frameworks/Python.framework/Versions/2.7/include/python2.7 -c cutils.c -o build/cutils.o
	clang -bundle -undefined dynamic_lookup -L/usr/local/lib build/cutils.o -o cutils.so

network:
	clang -fno-strict-aliasing -fno-common -dynamic -I/usr/local/include -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -I/usr/local/Cellar/python/2.7.8_2/Frameworks/Python.framework/Versions/2.7/include/python2.7 -c network.c -o build/network.o
	clang -bundle -undefined dynamic_lookup -L/usr/local/lib build/network.o -o network.so

clean:
	rm -f network.so
	rm -f cutils.so
	rm -rf build
	rm -f *.pyc

cython:
	python build.py build_ext --inplace
