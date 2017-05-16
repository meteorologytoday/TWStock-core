from bottle import route, run, static_file
import os

root = os.getcwd()

@route('/hello')
def hello():
    return "Hello World!"

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=root)

run(host='0.0.0.0', port=8888, debug=True)
