from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class CustomHTTPRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, endpoints, *args, **kwargs):
        self.endpoints = endpoints
        super().__init__(*args, **kwargs)

    def do_GET(self):
        path = self.path
        if path in self.endpoints:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"message": f"Endpoint {path} exists"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"message": "Not Found"}
            self.wfile.write(json.dumps(response).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=CustomHTTPRequestHandler, addr='', port=8000, endpoints=[]):
    def handler(*args, **kwargs):
        return handler_class(endpoints, *args, **kwargs)

    server_address = (addr, port)
    httpd = server_class(server_address, handler)
    httpd.serve_forever()

if __name__ == '__main__':
    run(endpoints=['/api', '/v9/dashboard'])
