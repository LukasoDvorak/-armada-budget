#!/usr/bin/env python3
"""
Armada Budget — local dev server
=================================
Serves the app from this folder on http://localhost:8080
SPA routing: any unknown path → index.html (same as Netlify _redirects)
Storage is handled by Dropbox (no local file saving needed).

Run:  python3 armada_local.py
Open: http://localhost:8080
"""

import http.server
import os

PORT = 8080
HOST = '127.0.0.1'

MIME = {
    '.html': 'text/html; charset=utf-8',
    '.js':   'application/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.css':  'text/css; charset=utf-8',
    '.svg':  'image/svg+xml',
    '.png':  'image/png',
    '.ico':  'image/x-icon',
    '.webmanifest': 'application/manifest+json',
}

class SPAHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        # Strip query string
        path = self.path.split('?')[0].split('#')[0]

        # Try to serve exact file
        local = os.path.join(os.getcwd(), path.lstrip('/'))
        if os.path.isfile(local):
            self.serve_file(local)
        else:
            # SPA fallback → index.html
            self.serve_file(os.path.join(os.getcwd(), 'index.html'))

    def serve_file(self, filepath):
        ext = os.path.splitext(filepath)[1].lower()
        mime = MIME.get(ext, 'application/octet-stream')
        try:
            with open(filepath, 'rb') as f:
                body = f.read()
            self.send_response(200)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            self.send_error(500, str(e))

    def log_message(self, fmt, *args):
        msg = fmt % args
        if 'favicon' not in msg:
            print(f'  {msg}')


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print('=' * 50)
    print('  ARMADA BUDGET — local server')
    print('=' * 50)
    print(f'  URL:    http://{HOST}:{PORT}')
    print(f'  Folder: {os.getcwd()}')
    print('  Ctrl+C to stop')
    print('=' * 50)

    import subprocess, threading
    def open_browser():
        import time; time.sleep(0.8)
        subprocess.Popen(['open', f'http://{HOST}:{PORT}'])
    threading.Thread(target=open_browser, daemon=True).start()

    with http.server.HTTPServer((HOST, PORT), SPAHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nServer stopped.')
