from http.server import BaseHTTPRequestHandler
import json

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
        if self.path == "/get-messages":
            msg = domain.get_messages()
            response = json.dumps(msg)
            self._set_response(200)
        elif self.path == "/ping":
            response = "pong"
            self._set_response(200)
        else:
            self._set_response(404)
        self.wfile.write(response.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        service_log("POST request! With new message: " + post_data.decode('utf-8'))
        domain = SecondaryDomain()
        if self.path == "/add-message":
            domain.add_message(data["id"], data["message"])
            self._set_response(200)
        else:
            self._set_response(404)
        self.wfile.write("".encode('utf-8'))