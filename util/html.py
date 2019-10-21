from flask import render_template

from config import *
from jinja2 import Environment, FileSystemLoader, select_autoescape


def ok(view, data={}, **args):
    options = {
        'status': 200,
    }
    options.update(args)
    body = render_template('%s.html.j2' % view, **data)

    res = Response(body, status=options['status'], mimetype='text/html')
    return res


def error(title, text='', description=False, errno=401):
    res = ok('error', {
        'title': title,
        'text': text,
        'description': description
    }, status=errno)
    return res
