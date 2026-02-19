from flask import Flask, request, Response
import requests
import re

app = Flask(__name__)

# Simple SQLi patterns (very small sample) - for demo only
SQLI_PATTERNS = [
    r"\b(or|and)\b\s+'?\d+'?\s*=\s*'?\d+'?",
    r"\b(or|and)\b\s+\'1\'\s*=\s*\'1\'",
    r"--",
    r";\s*drop\b",
]

UPSTREAM = 'http://user-service:8000'

def is_sqli(data: str) -> bool:
    if not data:
        return False
    for p in SQLI_PATTERNS:
        if re.search(p, data, re.IGNORECASE):
            return True
    return False

@app.route('/', defaults={'path': ''}, methods=['GET','POST','PUT','DELETE','PATCH','OPTIONS'])
@app.route('/<path:path>', methods=['GET','POST','PUT','DELETE','PATCH','OPTIONS'])
def proxy(path):
    # inspect query string and body for SQLi
    qs = request.query_string.decode('utf-8')
    body = request.get_data(as_text=True)
    if is_sqli(qs) or is_sqli(body):
        return Response('<html><body><h1>Access denied</h1><p>Request blocked by WAF</p></body></html>', status=403, mimetype='text/html')

    # forward request to upstream
    url = UPSTREAM.rstrip('/') + '/' + path
    headers = {k: v for k, v in request.headers if k.lower() != 'host'}
    resp = requests.request(request.method, url, headers=headers, params=request.args, data=request.get_data(), allow_redirects=False)
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
    return Response(resp.content, status=resp.status_code, headers=dict(headers))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
