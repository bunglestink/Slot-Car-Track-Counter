# An http server to serve the track counter frontend.

import json
import slotcars

from bottle import route
from bottle import run
from bottle import static_file


# Configure to listen on any hostname, port 80.
_HOSTNAME = '0.0.0.0'
_PORT = 80

_STATIC_FILE_ROOT = './static'

_TRACK_LISTENER_FILE = '/tmp/track-trips'


# Holds the race.
race = None


@route('/')
def Index():
  return static_file('html/index.html', root=_STATIC_FILE_ROOT)


@route('/static/<path:path>')
def StaticFiles(path):
  return static_file(path, _STATIC_FILE_ROOT)


@route('/api/race/start/<track_count>')
def StartRace(track_count):
  race.Start(track_count)


@route('/api/race/stop')
def StopRace():
  race.Stop()


@route('/api/race/stats')
def GetRaceStats():
  stats = race.GetStats()
  return json.dumps(stats)


try:
  race = slotcars.Race(_TRACK_LISTENER_FILE)
  slotcars.Cleanup()
  run(host=_HOSTNAME, port=_PORT)
finally:
  slotcars.Cleanup()

