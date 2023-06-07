from http.server import BaseHTTPRequestHandler

from SecondaryService.Logging import *
from SecondaryService.SecondaryDomain import SecondaryDomain

class SecondaryService(BaseHTTPRequestHandler):
    def _set_response(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        service_log("GET request!")
        domain = SecondaryDomain()
        domain.add_message("")
        if self.path == "/":
            self._set_response(200)
        else:
            self._set_response(404)
        self.wfile.write("".encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        service_log("POST request! With new message: " + post_data.decode('utf-8'))
        domain = SecondaryDomain()
        if self.path == "/":
            self._set_response(200)
        else:
            self._set_response(404)
        self.wfile.write("".encode('utf-8'))