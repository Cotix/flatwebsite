from config import *
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('views/'),
    autoescape=select_autoescape(['j2', 'html'])
)


def ok(view, data={}, **args):
    options = {
        'status': 200,
    }
    options.update(args)
    body = env.get_template('%s.html.j2' % view).render(data)
    res = Response(body, status=options['status'], mimetype='text/html')
    return res


def error(title, text='', description=False, errno=401):
    res = ok('error', {
        'title': title,
        'text': text,
        'description': description
    }, status=errno)
    return res
