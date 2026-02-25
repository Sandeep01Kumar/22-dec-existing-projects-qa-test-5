from flask import Flask, Response

app = Flask(__name__)


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
def catch_all(path):
    """Handle all HTTP requests on any path with a plain-text Hello World response.

    Replicates the original Node.js http.createServer() catch-all behavior:
    every request, regardless of URL path or HTTP method, receives an identical
    200 OK response with Content-Type text/plain and body 'Hello, World!\n'.
    """
    return Response('Hello, World!\n', status=200, content_type='text/plain')


if __name__ == '__main__':
    print('Server running at http://127.0.0.1:3000/')
    app.run(host='127.0.0.1', port=3000)
