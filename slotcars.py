# Slot car race logic manager.

import collections
import os
import subprocess

import config


class RaceManager(object):
  """Starts and stops slot car races and handles race state."""
  
  def __init__(self, track_listener_file):
    self._track_listener_file = track_listener_file
    self._track_listener_process = None

  def Start(self):
    """Starts a new race with the given number of tracks."""
    if self._track_listener_process:
      return
    cmd = [config.PYTHON_COMMAND, config.TRACK_LISTENER_FILE]
    self._track_listener_process = subprocess.Popen(cmd)

  def Stop(self):
    """Stops the current race, cleaning up any monitoring."""
    if self._track_listener_process:
      self._track_listener_process.kill()
    self._track_listener_process = None

  def GetStats(self):
    """Returns the current stats for the race.
    
    Returns:
      A dictionary where the keys are the track numbers and the values are
      the times the lap counter has been tripped at.  If there isn't a race
      currently running, None is returned.
    """
    if not self._track_listener_process:
      return None

    # If output file doesn't exist yet, return empty result.
    if not os.path.exists(config.TRACK_LISTENER_OUTPUT_FILE):
      return {}

    with open(config.TRACK_LISTENER_OUTPUT_FILE, 'r') as f:
      lines = f.readlines()

    # Note: Data will be sorted already, since it is logged sequentially.
    lap_times = collections.defaultdict(list)
    for line in lines:
      print 'Line: %s' % line
      track_s, time_s = line.split(config.TRACK_LISTENER_OUTPUT_FILE_DELIMETER)
      track = int(track_s)
      time = float(time_s.strip())
      lap_times[track].append(time)

    return lap_times

