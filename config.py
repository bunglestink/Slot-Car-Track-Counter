# Configuration for stock car track timings.

# The python command.
PYTHON_COMMAND = 'python'

# This file contains the output of the track monitor.
# The lines of the file each represnt a single instance of the track being 
# tripped, and are of the following form:
#
#   <track_number><delimeter><timestamp>
TRACK_LISTENER_OUTPUT_FILE = '/tmp/track-trips'

# The delimeter in the output file.
TRACK_LISTENER_OUTPUT_FILE_DELIMETER = ':'

# The name of the track listener file.
TRACK_LISTENER_FILE = 'track_listener.py'

