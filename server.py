import os
import urllib.parse
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

class CleanURLHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Extract path without query parameters or anchors
        parsed = urllib.parse.urlparse(path)
        clean_path = parsed.path
        
        # Get base filesystem path from standard implementation
        orig_path = super().translate_path(clean_path)
        
        # If path does not exist as-is, check if appending .html matches a file
        if not os.path.exists(orig_path) and not clean_path.endswith('.html') and not clean_path.endswith('/'):
            html_candidate = orig_path + '.html'
            if os.path.exists(html_candidate):
                return html_candidate
                
        return orig_path

    def end_headers(self):
        # Avoid stale caching during local development
        self.send_header('Cache-Control', 'no-cache, must-revalidate')
        super().end_headers()

if __name__ == '__main__':
    port = 8080
    server_address = ('', port)
    httpd = ThreadingHTTPServer(server_address, CleanURLHandler)
    print(f"Tony Hair Salon Server running with Clean URLs at http://localhost:{port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
