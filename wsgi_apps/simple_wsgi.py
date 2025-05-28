
def app(environ, start_response):
    from urllib.parse import parse_qs

    method = environ['REQUEST_METHOD']
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]

    if method == 'GET':
        query = parse_qs(environ.get('QUERY_STRING', ''))
        body = f"GET params: {query}\n"
    elif method == 'POST':
        try:
            size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            size = 0
        post_data = environ['wsgi.input'].read(size).decode('utf-8')
        post_params = parse_qs(post_data)
        body = f"POST params: {post_params}\n"
    else:
        body = f"Unsupported method: {method}"
    start_response(status, headers)
    return [body.encode('utf-8')]
