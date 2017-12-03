from collections import deque
from liblo import *
import sys, time

# Data class to hold the values of the 4 electrodes
# Queue used for quick realtime drawing
# member functions for file storage need to be added here so that it is directly stored to file
class Data:
    # Default Queue length
    def __init__(self, length = 1100):
        self.l_ear = deque(maxlen=length)
        self.l_forehead = deque(maxlen=length)
        self.r_forehead = deque(maxlen=length)
        self.r_ear = deque(maxlen=length)
    # Update Queue fixed size
    def increment (self, args):
        vl_ear, vl_forehead, vr_forehead, vr_ear = args
        self.l_ear.append(vl_ear)
        self.l_forehead.append(vl_forehead)
        self.r_forehead.append(vr_forehead)
        self.r_ear.append(vr_ear)
    # Create new Queues with different max length
    # Useful for window reshaping and FFT
    def set_length(self,LENGTH):
        self.l_ear = deque(maxlen=LENGTH)
        self.l_forehead = deque(maxlen=LENGTH)
        self.r_forehead = deque(maxlen=LENGTH)
        self.r_ear = deque(maxlen=LENGTH)

# Server that holds the Data class and Pyliblo communication
class PylibloServer(ServerThread):
    # Default port is 1234
    def __init__(self, PORT=1234):
        ServerThread.__init__(self, PORT)
        self.EEG = Data()
    # Change the window size
    def set_window(self,LENGTH):
        self.EEG.set_length(LENGTH)
    # When new values are sent data is updated automatically
    @make_method('/muse/eeg', 'ffff')
    def eeg_callback(self, path, args):
        self.EEG.increment(args)
