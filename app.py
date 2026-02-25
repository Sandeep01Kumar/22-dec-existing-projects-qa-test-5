from flask import Flask, Response
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__)


class _QuietRequestHandler(WSGIRequestHandler):
    """Custom WSGI request handler that suppresses version disclosure.

    Werkzeug's default handler advertises 'Werkzeug/x.y.z Python/x.y.z'
    in the HTTP ``Server`` header.  This subclass overrides the version
    string so that exact framework and runtime versions are never leaked
    to clients, mitigating targeted-attack risk from version fingerprinting.
    """

    def version_string(self):
        """Return a generic server identifier instead of version details."""
        return 'Flask'


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
def catch_all(path):
    """Handle all HTTP requests on any path with a plain-text Hello World response.

    Replicates the original Node.js http.createServer() catch-all behavior:
    every request, regardless of URL path or HTTP method, receives an identical
    200 OK response with Content-Type text/plain and body 'Hello, World!\n'.
    """
    return Response('Hello, World!\n', status=200, content_type='text/plain')


@app.after_request
def set_security_headers(response):
    """Apply security-hardening headers to every outgoing HTTP response.

    Removes the default Server header that exposes Werkzeug and Python
    version details, and injects standard security headers recommended by
    OWASP to reduce the attack surface of the application.
    """
    # Prevent MIME-type sniffing — browser must honour the declared Content-Type
    response.headers['X-Content-Type-Options'] = 'nosniff'

    # Deny framing entirely — this API has no reason to be embedded in an iframe
    response.headers['X-Frame-Options'] = 'DENY'

    # Restrictive default CSP — no resources should be loaded by this plain-text API
    response.headers['Content-Security-Policy'] = "default-src 'none'"

    return response


if __name__ == '__main__':
    print('Server running at http://127.0.0.1:3000/')
    app.run(host='127.0.0.1', port=3000, request_handler=_QuietRequestHandler)
