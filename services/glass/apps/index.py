import logging
import os
import re
import xml.sax
import sys

from core import resolve, render, redirect, parse_qs


_filename_ascii_strip_re = re.compile(r'[^A-Za-z0-9_.-]')
log = logging.getLogger(__name__)
log.setLevel('DEBUG')
log.addHandler(logging.StreamHandler())


class ContentHandler(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.obj = {}

    def startElement(self, name, attrs):
        self.data = ""

    def endElement(self, name):
        self.obj[name] = self.data
        self.data = ""

    def characters(self, content):
        self.data += content

    def __getitem__(self, name):
        return self.obj.get(name, '')


def secure_filename(filename):
    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, ' ')
    filename = str(_filename_ascii_strip_re.sub(
        '', '_'.join(filename.split()))) \
        .strip('._')
    return filename


def index(req):
    return render("index.html")


def save(req):
    if req.method != "POST":
        log.error('bead method')
        return redirect(resolve('error'))

    d = req.stream.read(req.stream_length).decode('ascii')
    d = parse_qs(d)

    if 'text' not in d or 'name' not in d:
        log.error('bead `name` or `text`')
        return render('error.html', {'message': "required `name` and `text`!"})

    text = d['text'][0]
    name = d['name'][0]

    # name = secure_filename(name)
    path = os.path.join('data', name)

    with open(path, 'w') as f:
        log.info('write to {0}'.format(path))
        f.write(text)

    next = req.get.get('next')
    if next:
        next = resolve(next[0])
    else:
        next = resolve("apps.index.get") + "?name=" + name

    return render('save.html', {
        'timeout': 2000,
        'next': next,
        'name': name,
    })


def get(req):
    name = req.get.get('name')
    if not name:
        return render('error.html', {'message': "No name!"})
    name = name[0]

    # name = secure_filename(name)
    path = os.path.join('data', name)
    if not os.path.exists(path):
        return render('error.html', {'message': "Not Exists!"})

    handler = ContentHandler()
    xml.sax.parse(path, handler)
    context = dict(name=handler['name'],
                   descr=handler['description'],
                   data=handler['data'])

    return render('xml.html', context)
