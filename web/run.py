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

@route('/query_stock')
def query_stock():
	return template('query_stock')

@route('/query_stock/engine')
	import QueryStock as qs
	from datetime import date
	no = response.forms.get('no')
	beg_date = date.strptime(response.forms.get('beg_date'), '%Y-%m-%d')
	end_date = date.strptime(response.forms.get('end_date'), '%Y-%m-%d')

	try:
		data = qs.query(no, beg_date, end_date, TWStock_root + '/data')
	except Exception as e:
		return {'error': str(e)}

	return dict(data)

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
