from http.server import BaseHTTPRequestHandler, HTTPServer
import json

httpd = None

class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    def get_endpoints(self):
        return []

    def do_GET(self):
        path = self.path
        endpoints = self.get_endpoints()
        if path in endpoints:
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

def handler_factory(endpoints):
    """
    Factory function to create a handler class with a customized get_endpoints method.
    """
    def get_endpoints():
        return endpoints

    # Return a new type dynamically creating a subclass of CustomHTTPRequestHandler
    return type(
        'CustomizedHandler',
        (CustomHTTPRequestHandler,),
        {'get_endpoints': staticmethod(get_endpoints)}
    )

def run(addr='', port=8000, endpoints=[]):
    global httpd
    handler_class = handler_factory(endpoints)
    server_address = (addr, port)
    httpd = HTTPServer(server_address, handler_class)
    print(f"Starting server on {port}...")
    httpd.serve_forever()

def stop():
    global httpd
    if httpd:
        httpd.shutdown()

if __name__ == '__main__':
    try:
        run(endpoints=['/api', '/v9/dashboard'])
    except KeyboardInterrupt:
        stop()
        print("\nServer stopped.")
