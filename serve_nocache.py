"""Local dev server for the UNIverse prototype that never lets the browser cache a stale copy.

Plain `python -m http.server` sends no Cache-Control header, so Chrome is free to reuse an old
cached page/stylesheet/script indefinitely (a plain reload doesn't revalidate) -- which makes an
edit look like it "didn't work" when it's really just the browser showing you yesterday's file.
This adds `Cache-Control: no-store` to every response so every request always hits disk fresh.

Usage: python serve_nocache.py [port]   (default port 8000)
"""
import sys
import http.server

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        super().end_headers()


if __name__ == '__main__':
    with http.server.ThreadingHTTPServer(('', PORT), NoCacheHandler) as httpd:
        print('Serving (no-cache) at http://localhost:%d/' % PORT)
        httpd.serve_forever()
