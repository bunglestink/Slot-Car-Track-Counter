
from bottle import route
from bottle import run
from bottle import static_file

# Configure to listen on any hostname, port 80.
_HOSTNAME = '0.0.0.0'
_PORT = 80

_STATIC_FILE_ROOT = './static'


@route('/')
def Index():
  return static_file('html/index.html', root=_STATIC_FILE_ROOT)


@route('/static/<path:path>')
def StaticFiles(path):
  return static_file(path, _STATIC_FILE_ROOT)


run(host=_HOSTNAME, port=_PORT)

