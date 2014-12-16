import logging
import os
import re
import sys
import traceback

PY3 = sys.version_info >= (3, 0, 0)

if PY3:
    from http.cookies import SimpleCookie
    from urllib.parse import parse_qs

    string_types = (str, )
else:
    from Cookie import SimpleCookie
    from urlparse import parse_qs

    string_types = (str, unicode)

__author__ = 'pahaz'
__indent__ = 0
log = logging.getLogger(__name__)
log.setLevel('DEBUG')
log.addHandler(logging.StreamHandler())


def log_function(f, sub_name=''):
    def _wrapper(*args, **kwargs):
        global __indent__
        log.debug("{0} -(call)-> {4}{1}(*{2}, **{3})"
                  .format(" " * __indent__ * 2, f.__name__, args, kwargs,
                          sub_name))
        __indent__ += 1
        ret = f(*args, **kwargs)
        __indent__ -= 1
        return ret

    return _wrapper


def log_class(match=".*"):
    def _wrapper(cls):
        allow = lambda s: re.match(match, s) and s not in (
            '__str__', '__repr__')
        for k, v in cls.__dict__.items():
            if not allow(k):
                continue
            if callable(v):
                f = log_function(v, cls.__name__ + '.')
                setattr(cls, k, f)
        return cls

    return _wrapper


def cached(f):
    def _wrapper(*args, **kwargs):
        k = args + tuple(kwargs.items())
        if k not in _wrapper._cache:
            _wrapper._cache[k] = f(*args, **kwargs)
        return _wrapper._cache[k]

    _wrapper._cache = {}
    return _wrapper


def import_string(import_name, silent=True):
    assert isinstance(import_name, string_types)
    import_name = str(import_name)
    try:
        if '.' in import_name:
            module, obj = import_name.rsplit('.', 1)
        else:
            return __import__(import_name)

        try:
            return getattr(__import__(module, None, None, [obj]), obj)
        except (ImportError, AttributeError):
            modname = module + '.' + obj
            __import__(modname)
            return sys.modules[modname]
    except ImportError as e:
        if not silent:
            raise


def parse_post(environ):
    try:
        request_body_size = int(environ.get("CONTENT_LENGTH", 0))
    except ValueError:
        request_body_size = 0

    request_body = environ["wsgi.input"].read(request_body_size)
    body_query_dict = parse_qs(request_body)

    return body_query_dict


def take_one_or_None(dict_, key):
    val = dict_.get(key)
    if type(val) in (list, tuple) and len(val) > 0:
        val = val[0]
    return val


def resolve(name):
    global router
    return router.resolve(name)


def render(name, context=None):
    global template
    if not context:
        context = {}
    return 200, template.render(name, context)


def redirect(url):
    return 200, "<script>document.location.href='{0}'</script>"\
        .format(url)


@log_class()
class Router(object):
    def __init__(self):
        self.__resolve = {}
        self.__paths = {}
        self.__name = {}

    def route(self, request_path, request_data):
        callback = self.__paths.get(request_path)
        try:
            if callback and callable(callback):
                res = callback(request_data)
            else:
                res = self.default_response(request_data)
        except Exception as e:
            res = self.error_response(request_data, e)
        return res

    def add_route(self, path, callback, name=None):
        if isinstance(callback, string_types):
            callback = import_string(callback)

        self.__paths[path] = callback
        self.__resolve[callback] = path
        if name:
            self.__name[name] = path

    def resolve(self, name):
        path = self.__name.get(name)
        if not path:
            callback = import_string(name)
            path = self.__resolve.get(callback)
        return path or '/'

    def rm_route(self, path):
        del self.__paths[path]

    def default_response(self, *args):
        return 404, "Nooo 404!"

    def error_response(self, req, error):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb = ''.join(traceback.format_tb(exc_traceback))
        response_body = "<h1>ERROR: {1}</h1><pre>{0}</pre>".format(tb, str(error))
        return 500, response_body


class Template(object):
    def __init__(self, global_context=None, base_dir="templates"):
        self.global_context = global_context or {}
        self.base_dir = base_dir

    def render(self, name, context):
        tpl = self._load(name)
        c_tpl = self._compile(tpl)
        return c_tpl(**context)

    #@cached
    def _load(self, name):
        path = os.path.join(self.base_dir, name)
        if not os.path.exists(path):
            raise RuntimeError('template {0} not exists'.format(name))

        with open(path) as f:
            return f.read()

    #@cached
    def _compile(self, tpl):
        lst = re.split(r"""(\{\{.*?\}\})""", tpl)
        global_context = self.global_context

        def _f(**context):
            tmp = []
            line = 0
            for x in lst:
                i = x.count('\n')
                line += i
                if x.startswith('{{') and x.endswith('}}'):
                    x = x[2:-2].strip()
                    try:
                        x = str(eval(x, global_context, context))
                    except Exception as e:
                        x = "<span style='color: red'>`{1}` - {0}</span>" \
                            .format(e, x)

                tmp.append(x)
            return ''.join(tmp)

        return _f


router = Router()
template = Template({
    'resolve': resolve,
})
