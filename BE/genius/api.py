import json
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from genius.runner import run_pipeline


def app(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    if path == '/run' and environ['REQUEST_METHOD'] == 'POST':
        try:
            length = int(environ.get('CONTENT_LENGTH', 0))
            body = environ['wsgi.input'].read(length)
            data = json.loads(body.decode('utf-8'))
            repo = data.get('repo')
            if not repo:
                start_response('400 Bad Request', [('Content-Type', 'application/json')])
                return [json.dumps({'error': 'missing repo field'}).encode('utf-8')]

            res = run_pipeline(repo, dest_root='./tmp_repos', outputs_root='./outputs')
            start_response('200 OK', [('Content-Type', 'application/json')])
            return [json.dumps(res).encode('utf-8')]
        except Exception as e:
            start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
            return [json.dumps({'error': str(e)}).encode('utf-8')]

    # simple index
    if path == '/':
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'Codebase Genius API. POST JSON {"repo": "<path-or-git>"} to /run']

    start_response('404 Not Found', [('Content-Type', 'text/plain')])
    return [b'Not Found']


def serve(port=8000):
    print(f'Starting Codebase Genius API on http://0.0.0.0:{port}')
    with make_server('0.0.0.0', port, app) as httpd:
        httpd.serve_forever()


if __name__ == '__main__':
    serve(8000)
