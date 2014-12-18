from core import router, SimpleCookie, parse_qs, string_types


router.add_route("/",
                 "apps.index.index",
                 name="index")

router.add_route("/save",
                 "apps.index.save",
                 name="save")

router.add_route('/get',
                 "apps.index.get")

router.add_route('/secret',
                 "apps.test.secret",
                 name="secret")

INSTALLED = (
    'index',
    'test',
)

for x in INSTALLED:
    __import__("apps." + x)


def application(environ, start_response):
    global router

    path = environ.get('PATH_INFO') or '/'
    method = (environ.get('REQUEST_METHOD') or 'GET').upper()
    get = parse_qs(environ.get('QUERY_STRING', ''))
    cookies = SimpleCookie(environ.get('HTTP_COOKIE', ''))
    stream = environ["wsgi.input"]
    stream_length = int(environ.get("CONTENT_LENGTH") or 0)

    request = type('', (object, ), locals())

    # TODO: You can add this interesting line
    # print(parse_http_post_data(environ))
    # log.debug("The request ENV: {0}".format(repr(environ)))

    http_status_code, response_body = router.route(path, request)
    if isinstance(response_body, string_types):
        response_body = response_body.encode()

    response_status = "200 OK" if 200 == http_status_code else "400 WTF"
    response_headers = [("Content-Type", "text/html")]

    start_response(response_status, response_headers)
    return [response_body]


if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    httpd = make_server('', 8001, application)
    print("Serving on port 8001...")

    # Serve until process is killed
    httpd.serve_forever()
