import http.server
import ssl
import os

# Define the handler to serve a simple response
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/5fe9f194d0bb6ea1bef4bec10bcbe5d389bdc226cf91007952681850c79e3abe97612adec895805d4e975fafa488a3375e00e39cd5046a20c1f6d8b57a96ace6":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes("d5d9421513acc18a9988a2157ee9b1f32ae8471f", 'utf-8'))
        elif self.path == "/ead40c8582f4fc25805ed0cf895b2d28cb410c8cd7f3e99302575a03cc971eba393cea75c3fafdfb5d262a8314f1e8f72c8145e9e479fdc0160d5e6d6f7a7498":
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

context.load_cert_chain(keyfile="key.pem", certfile="cert.pem")

context.load_verify_locations("ca-cert.pem")

context.verify_mode = ssl.CERT_REQUIRED

# Wrap the server socket with SSL
httpd.socket = context.wrap_socket(httpd.socket,
                               server_side=True,do_handshake_on_connect=False)

# Start the server
print(f"Serving on https://0.0.0.0:{port}")
httpd.serve_forever()