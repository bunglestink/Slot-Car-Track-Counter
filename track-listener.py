# This script listens to an arduino's serial port to monitor slot car tracks
# using distance sensors.
#
# This determines when a car completes a lap by logging the time a "significant"
# change in that track's sensor occurs.  This is intended to be the backend
# to a web interface that will launch this script at the start of a race.  The
# web interface will poll the output file of this script.
# 
# The arduino device monitors n distance sensors and broadcasts the results
# over its serial link as a json list, where each element has the following
# format:
#   track: The number of the track this the sensor is for.
#   value: The distance value for this track.


import collections
import json
import logging
import os
import serial
import time


_ARDUINO_DEVICE_PATH = '/dev/ttyACM0'
_BAUD_RATE = 9600

# Tolerate differences up to 5%.
_DIFFERENCE_THRESHOLD = .05
_WAIT_AFTER_TRIP_SECONDS = 3

_OUTPUT_FILE = '/tmp/track-trips'


class Arduino(object):
  """Simple class to abstract away the arduino communication."""

  def __init__(self, device_path, baud_rate):
    self._serial = serial.Serial(device_path, baud_rate)
    # Get an average starting value over 10 reads.
    self.initial_values = self.GetAverageValues(10)

  def GetValues(self):
    serial_value = self._serial.readline()
    return json.loads(serial_value)

  def GetAverageValues(self, reads):
    results = {}
    all_values = collections.defaultdict(list)
    total_read = 0
    while total_read < reads:
      values = self.GetValues()
      for track_record in values:
        track = track_record['track']
        value = track_record['value']
        all_values[track].append(value)
      total_read += 1
    
    for track, values in all_values.iteritems():
      value_sum = sum(values)
      results[track] = int(value_sum / reads)
    return results

  def FlushStream(self):
    self._serial.flushInput()


def IsArduinoDevicePresent():
  return os.path.exists(_ARDUINO_DEVICE_PATH)


def DeleteOutputFileIfExists():
  if os.path.exists(_OUTPUT_FILE):
    os.remove(_OUTPUT_FILE)


def IsValueSignificantlyDifferent(base_value, value):
  difference = abs(base_value - value)
  difference_percentage = float(difference) / base_value
  return difference_percentage > _DIFFERENCE_THRESHOLD


def LogTripTime(track):
  trip_timestamp = time.time()
  with open(_OUTPUT_FILE, 'a') as f:
    # TODO: Determine what the file format should be.
    f.write('%s:%r\n' % (track, trip_timestamp))


def Main():
  # Check if arduino is present, sleep until ready.
  logging.info('checking for arduino...')
  while not IsArduinoDevicePresent():
    time.sleep(3)

  logging.info('connecting to arduino...')
  arduino = Arduino(_ARDUINO_DEVICE_PATH, _BAUD_RATE)
  
  # Clear the output file if present by deleting.
  DeleteOutputFileIfExists()

  # Now loop forever, reading when there are significant changes.
  while True:
    values = arduino.GetValues()
    for track_record in values:
      track = track_record['track']
      value = track_record['value']
      if IsValueSignificantlyDifferent(arduino.initial_values[track], value):
        print 'track %s tripped!' % track
        LogTripTime(track)
        # TODO: This WON'T work with multiple tracks!
        time.sleep(_WAIT_AFTER_TRIP_SECONDS)
        arduino.FlushStream()


if __name__ == '__main__':
  Main()

