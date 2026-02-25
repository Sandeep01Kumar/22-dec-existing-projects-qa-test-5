"""Flask application entry point — replaces the original Node.js server.js.

This module implements a minimal HTTP server using Flask that replicates the
exact behavior of the original Node.js http.createServer() implementation:
every incoming request, regardless of URL path or HTTP method, receives an
identical 200 OK response with Content-Type text/plain and body
'Hello, World!\n' (14 bytes including the trailing newline).

Usage:
    pip install -r requirements.txt
    python app.py

The server binds to 127.0.0.1 on port 3000, matching the original Node.js
server configuration.
"""

from flask import Flask, Response

app = Flask(__name__)


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
def catch_all(path):
    """Handle all HTTP requests on any path with a plain-text Hello World response.

    Replicates the original Node.js http.createServer() catch-all behavior:
    every request, regardless of URL path or HTTP method, receives an identical
    200 OK response with Content-Type text/plain and body 'Hello, World!\\n'.

    Args:
        path: The URL path requested by the client. Captured by Flask's path
              converter but unused, since all paths return the same response.

    Returns:
        A Flask Response object with body 'Hello, World!\\n', HTTP status 200,
        and Content-Type set to text/plain.
    """
    return Response('Hello, World!\n', status=200, content_type='text/plain')


if __name__ == '__main__':
    print('Server running at http://127.0.0.1:3000/')
    app.run(host='127.0.0.1', port=3000)
