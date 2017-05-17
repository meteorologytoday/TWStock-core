from bottle import route, run, static_file, template
import os

root = os.getcwd()

@route('/')
def hello():
    return template('index')

@route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root="%s/static" % (root,))

@route('/analysis01')
def analysis01():
	return template('analysis01')

run(host='0.0.0.0', port=8888, debug=True)
