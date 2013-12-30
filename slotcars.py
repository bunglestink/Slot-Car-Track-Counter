# Slot car race logic.

import os


_TRACK_MONITOR_PROCESS_FILE = '/tmp/track-monitor-process'


class Race(object):
  """Encapsulates a slot car race.""" 
  
  def __init__(self, track_listener_file):
    self._track_listener_file = track_listener_file

  def Start(self, track_count):
    """Starts a new race with the given number of tracks."""
    # TODO: Implement me.

  def Stop(self):
    """Stops the current race, cleaning up any monitoring."""
    # TODO: Implement me.

  def GetStats(self):
    """Returns the current stats for the race."""
    # TODO: Implement me.
    return None


def Cleanup():
  if os.path.exists(_TRACK_MONITOR_PROCESS_FILE):
    with open(_TRACK_MONITOR_PROCESS_FILE, 'r') as f:
      process_number = f.read().strip()
      os.system('kill -9 %s' % process_number)
    os.remove(_TRACK_MONITOR_PROCESS_FILE)

