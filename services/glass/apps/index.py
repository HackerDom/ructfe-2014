import os
import re

from core import resolve, render, redirect, parse_qs


__author__ = 'pahaz'
_filename_ascii_strip_re = re.compile(r'[^A-Za-z0-9_.-]')


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
        return redirect(resolve('error'))

    d = req.stream.read(req.stream_length).decode('ascii')
    d = parse_qs(d)

    if 'text' not in d or 'name' not in d:
        return render('error.html', {'message': "required `name` and `text`!"})

    text = d['text'][0]
    name = d['name'][0]

    # name = secure_filename(name)
    path = os.path.join('data', name)

    with open(path, 'w') as f:
        f.write(text)

    return 200, name


def get(req):
    name = req.get.get('name')
    if not name:
        return render('error.html', {'message': "No name!"})
    name = name[0]

    # name = secure_filename(name)
    path = os.path.join('data', name)
    if not os.path.exists(path):
        return render('error.html', {'message': "Not Exists!"})

    with open(path, 'r') as f:
        content = f.read()

    return 200, content
