"""Contains server that holds Pyliblo communication"""
from liblo import *
from pylsl import local_clock
import threading


def process(data, timestamp, index, outlet):
    """Callback function for pushing data to an lsl outlet.

    Args:
        data: The data being pushed through the lsl outlet. Must be an array with size specified by the number of
            channels in pylsl.StreamInfo.
        timestamp: The time at which the data sample occurred, such as through pylsl.local_clock(), etc.
        index: For testing purposes; index at which the sample occurred.
        outlet: pylsl outlet to which data is pushed.
    """
    outlet.push_sample(data, timestamp)


class PylibloServer(ServerThread):
    """Class for 2014 muse hardware.

    Opens port for communication between muse headset and streaming outlet.

    Attributes:
        port: Number specifying which port the muse is streaming through.
        callback: Function used to publish data. Use process() for this purpose.
        outlet: pylsl outlet to which data is pushed.
    """

    def __init__(self, port=1234, callback=None, outlet=None):
        """Initialize."""
        ServerThread.__init__(self, port)
        # connection start time (needed for time-stamping)
        self.start_time = local_clock()

        # frequency multiplier
        self.freq_mult = 1. / 220

        # running index for timestamp
        self.time_index = 0

        # callback function for lsl data push
        self.callback = callback

        # lsl outlet to push data to
        self.outlet = outlet

        self._active = False
        self._kill_signal = threading.Event()

    def __del__(self):
        # Break out of the loop of data collection.
        self._kill_signal.set()

    def connect(self):
        """Start a new thread and connect to """
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