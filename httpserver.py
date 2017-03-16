import BaseHTTPServer, sys, base64

b64_data = ""

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	# define what to do with GET requests
	def do_GET(s):
		global b64_data
		s.send_response(200)
	  	b64_data = s.path[2:]
	def log_message(self, format, *args):
        	return

# receive some base64 data and convert it to ascii
def keep_running():
	global b64_data
	if b64_data == "66696e65": # stop
		b64_data = ""
		return False
	else:
		try:
			data = base64.b64decode(b64_data)
			sys.stdout.write(data)
		except Exception, e:
			print "\nException: "+str(e)		
		return True

# listen on 0.0.0.0:80 till b64_data is not empty
def listen():
	httpd = BaseHTTPServer.HTTPServer(('', 80), MyHandler)
	while keep_running():
		httpd.handle_request()
