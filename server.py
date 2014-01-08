# An http server to serve the track counter frontend.

import json

import race_manager as race_manager_module

from bottle import route
from bottle import run
from bottle import static_file


# Configure to listen on any hostname, port 80.
_HOSTNAME = '0.0.0.0'
_PORT = 80

_STATIC_FILE_ROOT = './static'

_TRACK_LISTENER_FILE = '/tmp/track-trips'


# Global race manager object.
race_manager = None


@route('/')
def Index():
  return static_file('html/index.html', root=_STATIC_FILE_ROOT)


@route('/static/<path:path>')
def StaticFiles(path):
  return static_file(path, _STATIC_FILE_ROOT)


@route('/api/race/start')
def StartRace():
  race_manager.Start()


@route('/api/race/stop')
def StopRace():
  race_manager.Stop()


@route('/api/race/stats')
def GetRaceStats():
  stats = race_manager.GetStats()
  return json.dumps(stats)


try:
  race_manager = race_manager_module.RaceManager(_TRACK_LISTENER_FILE)
  run(host=_HOSTNAME, port=_PORT)
finally:
  race_manager.Stop()

