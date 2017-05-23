from bottle import route, run, static_file, template, abort, response
import os, json
from helper import status

web_root = os.getcwd()
TWStock_root = os.path.abspath("%s/../" % os.getcwd())

@route('/')
def hello():
	return template('index')

@route('/static/<filename:path>')
def server_static(filename):
	global web_root
	return static_file(filename, root="%s/static" % (web_root,))

@route('/analysis01')
def analysis01():
	return template('analysis01')

@route('/control_panel')
def control_panel():
	return template('control_panel')

@route('/status/<what>')
def status(what):
	global web_root
	p = "%s/status/downloading" % (web_root,)
	
	if what == 'downloading':
		if os.path.isfile(p):
			with open(p, 'r') as f:
				s = json.load(f)
				return s
		else:
			return {'status': 'idle'}

	abort(404)
			
			
	

run(host='0.0.0.0', port=8888, debug=True)
