# An http server to serve the track counter frontend.

from bottle import route
from bottle import run
from bottle import static_file

# Configure to listen on any hostname, port 80.
_HOSTNAME = '0.0.0.0'
_PORT = 80

_STATIC_FILE_ROOT = './static'

_TRACK_MONITOR_PROCESS_FILE = '/tmp/track-monitor-process'

@route('/')
def Index():
  return static_file('html/index.html', root=_STATIC_FILE_ROOT)


@route('/static/<path:path>')
def StaticFiles(path):
  return static_file(path, _STATIC_FILE_ROOT)


@route('/api/race/start')
def StartRace():
  pass


@route('/api/race/stop')
def StopRace():
  pass


@route('/api/race/stats')
def GetRaceStats():
  pass


def Setup():
  pass


def Shutdown():
  pass


try:
  Setup()
  run(host=_HOSTNAME, port=_PORT)
finally:
  Shutdown()

