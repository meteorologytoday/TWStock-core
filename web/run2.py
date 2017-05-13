import http.server
import socketserver

PORT = 8888

Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(('', PORT), Handler) 
print("serving at port", PORT)
httpd.serve_forever()
