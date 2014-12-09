#!/usr/bin/env python3

from enum import Enum
import random
import sys
import urllib.error
import urllib.parse
import urllib.request


DEBUG = 0
PORT = 8000

AGENTS = [
    "Ubuntu APT-HTTP/1.3 (0.7.23.1ubuntu2)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.215 Safari/535.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16",
    "curl/7.19.5 (i586-pc-mingw32msvc) libcurl/7.19.5 OpenSSL/0.9.8l zlib/1.2.3",
    "Emacs-W3/4.0pre.46 URL/p4.0pre.46 (i686-pc-linux; X11)",
    "Mozilla/5.0 (X11; U; Linux i686; en-us) AppleWebKit/531.2+ (KHTML, like Gecko) Safari/531.2+ Epiphany/2.29.5",
    "Mozilla/5.0 (X11; U; Linux armv61; en-US; rv:1.9.1b2pre) Gecko/20081015 Fennec/1.0a1",
    "Mozilla/5.0 (Windows NT 7.0; Win64; x64; rv:3.0b2pre) Gecko/20110203 Firefox/4.0b12pre",
    "Mozilla/5.0 (X11; Linux i686; rv:6.0.2) Gecko/20100101 Firefox/6.0.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Linux; U; Android 1.1; en-gb; dream) AppleWebKit/525.10+ (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/4.5 RPT-HTTPClient/0.3-2",
    "Mozilla/5.0 (compatible; Konqueror/4.0; Linux) KHTML/4.0.5 (like Gecko)",
    "Links (2.1pre31; Linux 2.6.21-omap1 armv6l; x)",
    "Lynx/2.8.5dev.16 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.6b",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100508 SeaMonkey/2.0.4",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0 C; .NET4.0E; InfoPath.3; Creative AutoUpdate v1.40.02)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; GTB6.4; .NET CLR 1.1.4322; FDM; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.4506.2152; .NET CLR 3.5.307 29)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows 98; Rogers Hi�Speed Internet; (R1 1.3))",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6",
    "Opera/9.80 (J2ME/MIDP; Opera Mini/4.2.13221/25.623; U; en) Presto/2.5.25 Version/10.54",
    "Opera/9.80 (J2ME/MIDP; Opera Mini/5.1.21214/19.916; U; en) Presto/2.5.25",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Wget/1.8.1"
]


class ExitCode(Enum):
    OK = 101
    NOFLAG = 102
    MUMBLE = 103
    DOWN = 104
    ERROR = 110


class ServiceChecker:
    NO_CONNECT = "Could not connect to the service"
    SAVE_ERROR = "Could not save data"
    READ_ERROR = "Could not read data"
    PAGE_CORRUPTED = "Answer for save page is corrupted"
    MAINPAGE_CORRUPTED = "Main page is corrupted"
    FLAG_NOT_FOUND = "Flag not found"

    def __init__(self, ip):
        self.ip = ip
        self.baseurl = "http://{}:{}".format(ip, PORT)

    def _urlopener(self, url, data=None, headers=None):
        if not headers:
            headers = {}

        headers['User-Agent'] = random.choice(AGENTS)

        if data:
            data = urllib.parse.urlencode(data).encode('utf-8')

        return urllib.request.urlopen(
            urllib.request.Request(
                urllib.parse.urljoin(self.baseurl, url), headers=headers),
            data=data)

    @staticmethod
    def _done(code, message="", log=""):
        if DEBUG and code == ExitCode.OK:
            message = "\nOK"

        print(message, end='')
        print(log, end='', file=sys.stderr)
        sys.exit(code.value)

    @staticmethod
    def _create_xml(id_, flag):
        def rand_str():
            abc = 'QWERTYUIOPLKJHGFDSAZXCVBNM'
            n = random.randint(10, 100)
            return ''.join(random.choice(abc) for _ in range(n))

        return '''<?xml version="1.0" encoding="utf-8"?>
        <picture>
            <name>{name}</name>
            <description>{descr}</description>
            <data>{data}</data>
        </picture>
        '''.format(name=id_, descr=rand_str(), data=(flag + rand_str()))

    @staticmethod
    def _assert_in(what, where, reason):
        if what not in where:
            ServiceChecker._done(ExitCode.MUMBLE, reason)

    @staticmethod
    def _assert_not_in(what, where, reason):
        if what in where:
            ServiceChecker._done(ExitCode.MUMBLE, reason)

    def check(self, id_, flag):
        with self._urlopener('') as page:
            if page.status != 200:
                ServiceChecker._done(ExitCode.DOWN, ServiceChecker.NO_CONNECT)

            content = page.read().decode('utf-8')

            ServiceChecker._assert_not_in('Error', content,
                ServiceChecker.MAINPAGE_CORRUPTED)

            for word in ['input', 'save', 'get']:
                ServiceChecker._assert_in(word, content,
                    ServiceChecker.MAINPAGE_CORRUPTED)

        ServiceChecker._done(ExitCode.OK)

    def put(self, id_, flag):
        data = {'name': id_, 'text': ServiceChecker._create_xml(id_, flag)}
        with self._urlopener('/save', data=data) as page:
            if page.status != 200:
                ServiceChecker._done(ExitCode.DOWN, ServiceChecker.NO_CONNECT)

            content = page.read().decode('utf-8')

            ServiceChecker._assert_not_in('Error', content,
                ServiceChecker.SAVE_ERROR)

            for word in ['OK', 'javascript']:
                ServiceChecker._assert_in(word, content,
                    ServiceChecker.PAGE_CORRUPTED)

        ServiceChecker._done(ExitCode.OK)

    def get(self, id_, flag):
        with self._urlopener('/get?name={}'.format(id_)) as page:
            if page.status != 200:
                ServiceChecker._done(ExitCode.DOWN, ServiceChecker.NO_CONNECT)

            content = page.read().decode('utf-8')

            ServiceChecker._assert_not_in('Error', content,
                ServiceChecker.READ_ERROR)

            ServiceChecker._assert_in(flag, content,
                ServiceChecker.FLAG_NOT_FOUND)

        ServiceChecker._done(ExitCode.OK)


def main():
    if len(sys.argv) < 3:
        sys.exit("Usage: mode ip [id flag]")
    if len(sys.argv) == 5:
        (mode, ip, id_, flag) = sys.argv[1:5]
    else:
        (mode, ip) = sys.argv[1:3]
        id_, flag = None, None
    chk = ServiceChecker(ip)
    try:
        {'check': chk.check, 'put': chk.put, 'get': chk.get}[mode](id_, flag)
    except Exception as e:
        ServiceChecker._done(ExitCode.ERROR, "exitcode={}".format(e))


if __name__ == '__main__':
    main()
