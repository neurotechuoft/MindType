"""Contains server that holds Pyliblo communication"""
from liblo import *
from pylsl import local_clock


class PylibloServer(ServerThread):
    """class for 2014 muse hardware"""

    def __init__(self, port=1234, callback=None):
        """Initialize"""
        ServerThread.__init__(self, port)
        # connection start time (needed for timestamping)
        self.start_time = local_clock()
        # frequency multiplier
        self.freq_mult = 1. / 220
        # running index for timestamp
        self.time_index = 0
        # callback function for lsl data push
        self.callback = callback

        # When new values are sent data is updated automatically

    @make_method('/muse/eeg', 'ffff')
    def eeg_callback(self, path, args):
        """callback for receiving a sample

        - assuming the hardware sends samples at a stable 220 Hz
        - keep running index of every 4 values (from each channel)
        - calculate timestamp by multiplying index by frequency multiplier
        """
        timestamp = self.time_index * self.freq_mult + self.start_time
        self.callback(args, timestamp, self.time_index)
        self.time_index += 1
