import http.server
import ssl
import os

# Define the handler to serve a simple response
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/NbTA/MlGXQYBJDslhgeWkJlXAQcHBoaCDcs6vgeCWiD384GOd9+AWh4T8zI8s9ZxPig1tMD8yUZdBgEkOyWGB5aQmVcBBwcGhoINyzq+B4LxRi4QhuuqxMUO":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(os.environ['FLAG'], 'utf-8'))
        else:
            self.send_error(400)

port = int(os.environ['PYTHON_PORT'])

# Set up the server
httpd = http.server.HTTPServer(('0.0.0.0', port), MyHandler)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

context.load_cert_chain(keyfile="key.pem", certfile="cert.pem", password="pempassword")

# Wrap the server socket with SSL
httpd.socket = context.wrap_socket(httpd.socket,
                               server_side=True,do_handshake_on_connect=False)

# Start the server
print(f"Serving on https://0.0.0.0:{port}")
httpd.serve_forever()