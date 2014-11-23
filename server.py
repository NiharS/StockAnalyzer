import os
import SimpleHTTPServer
import SocketServer


PORT = int(os.getenv('VCAP_APP_PORT', '8000'))

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(("",PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
