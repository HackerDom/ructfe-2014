from io import BytesIO
import os
import sys
import unittest

__author__ = 'pahaz'


class TestTemplate(unittest.TestCase):
    def test_compile(self):
        from core import Template
        t = Template()

        f = t._compile("== {{ 2+3 + sudud }} == wdawd")
        self.assertEqual(f(sudud=2), "== 7 == wdawd")
        self.assertIn("span style='color: red'", f())

        tpl = ''''awfawkfawf

        {{ s1 }} wdawdaw{{

        daw }}

         {{s2 }}

        '''

        f = t._compile(tpl)
        t = f(s1="31337", s2="31339")
        self.assertIn("31337", t)
        self.assertIn("31339", t)
        self.assertNotIn("span style='color: red'", t)

    def test_load(self):
        from core import Template
        t = Template()

        z = t._load('test.html')
        self.assertIn('{{title}}', z)

    def test_global_context(self):
        from core import Template
        t = Template(global_context={'zzz': "228"})

        f = t._compile("awfaiwf {{ zzz }} awdawd")
        z = f()
        self.assertIn("228", z)
        self.assertNotIn("span style='color: red'", z)

        f = t._compile("awfa {{zz}} iwf {{ zzz }} awdawd")
        z = f(zz="081")
        self.assertIn("081", z)
        self.assertIn("228", z)
        self.assertNotIn("span style='color: red'", z)


def read_content(path):
    with open(path, 'r') as f:
        return f.read()


def write_content(path, data):
    with open(path, 'w') as f:
        f.write(data)


class TestAppIndex(unittest.TestCase):
    def test_index(self):
        s, h, body = go("GET", '/')
        self.assertIn("form", body)
        self.assertNotIn("span style='color: red'", body)

    def test_save(self):
        path = os.path.join('data', 'f1.txt')
        if os.path.exists(path):
            os.remove(path)

        s, h, body = go("POST", '/save', "name=f1.txt&text=secretiki")
        self.assertTrue(os.path.exists(path))
        self.assertNotIn("span style='color: red'", body)
        self.assertEqual(read_content(path), 'secretiki')

    def test_get(self):
        path = os.path.join('data', 'f2.txt')
        write_content(path, """<?xml version="1.0" encoding="utf-8"?>
<picture>
    <name>Name picture</name>
    <description>Picture description</description>
    <data>Picture data;'</data>
</picture>
""")

        s, h, body = go("GET", '/get', query='name=f2.txt')
        self.assertNotIn("span style='color: red'", body)
        self.assertIn("<h1>Picture 'Name picture'</h1>", body)
        os.remove(path)


def run_with_cgi(application, method, url, _in, _length, query):
    environ = dict()
    environ['wsgi.input'] = _in
    environ['CONTENT_LENGTH'] = _length
    environ['wsgi.errors'] = sys.stderr
    environ['wsgi.version'] = (1, 0)
    environ['wsgi.multithread'] = False
    environ['wsgi.multiprocess'] = True
    environ['wsgi.run_once'] = True
    environ['wsgi.url_scheme'] = 'http'
    environ['PATH_INFO'] = url
    environ['REQUEST_METHOD'] = method.upper()
    environ['QUERY_STRING'] = query

    _status = None
    _response_headers = None

    def start_response(status, response_headers):
        nonlocal _status, _response_headers
        _status = status
        _response_headers = response_headers

    result = application(environ, start_response)
    output = [data for data in result]
    return _status, _response_headers, output


def go(method="GET", url="/", data="", query=""):
    from wsgi import application
    _io = BytesIO(data.encode())
    _length = len(data)
    _status, _response_headers, _body = run_with_cgi(
        application, method, url, _io, _length, query)
    print('-'*79)
    print('STATUS: {0}'.format(_status))
    print('H: {0}'.format(_response_headers))
    print(_body)
    print('-'*79)
    assert _status == "200 OK", "STATUS != 200: {0}".format(_status)
    return _status, _response_headers, b''.join(_body).decode()


if __name__ == "__main__":
    print(go())
    print(go('POST', '/save', "aaa=2"))
    unittest.main()
