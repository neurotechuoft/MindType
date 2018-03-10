"""Contains server that holds Pyliblo communication"""
from liblo import *
from pylsl import local_clock
import threading


def process(data, timestamp, index, outlet):
    outlet.push_sample(data, timestamp)

    # index for testing purposes; check how many samples sent


class PylibloServer(ServerThread):
    """class for 2014 muse hardware"""

    def __init__(self, port=1234, callback=None, outlet=None):
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
        # lsl outlet to push data to
        self.outlet = outlet
        # When new values are sent data is updated automatically
        self._active = False
        self._kill_signal = threading.Event()

    def __del__(self):
        # Break out of the loop of data collection.
        self._kill_signal.set()

    def connect(self):
        if self._active:
            raise RuntimeError("Stream already active.")
        else:
            self._thread = threading.Thread(target=self.start(), name='Muse-connection')
            self._thread.daemon = True
            self._thread.start()
            self._active = True
            print('Connected to Muse. Streaming data')
        return

    @make_method('/muse/eeg', 'ffff')
    def eeg_callback(self, path, args):
        """callback for receiving a sample

        - assuming the hardware sends samples at a stable 220 Hz
        - keep running index of every 4 values (from each channel)
        - calculate timestamp by multiplying index by frequency multiplier
        """
        timestamp = self.time_index * self.freq_mult + self.start_time
        self.callback(args, timestamp, self.time_index, self.outlet)
        self.time_index += 1