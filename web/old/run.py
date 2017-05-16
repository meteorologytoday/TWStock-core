import http.server
import json
from urllib.parse import urlparse
import subprocess

class S(http.server.BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_GET(self):
		self._set_headers()
		print(self.path)
		parsed_path = urlparse(self.path)
		self.wfile.write(bytes('<html><body>test : %s</body></html>' % (self.path), 'UTF-8'))

	def do_POST(self):
		self._set_headers()
		parsed_path = urlparse(self.path)
		self.wfile.write(self.path)

	def do_HEAD(self):
		self._set_headers()

def run(server_class=http.server.HTTPServer, handler_class=S, port=8888):
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print('Starting httpd...')
	httpd.serve_forever()

if __name__ == "__main__":
	from sys import argv

	if len(argv) == 2:
		run(port=int(argv[1]))
	else:
		run()
