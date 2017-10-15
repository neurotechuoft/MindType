import json
import sys
import numpy as np
import time
import zmq
import csv
from biosppy.signals import tools as st
from biosignals.BioSignal import BioSignal
from scipy.signal import butter, lfilter



class Interface:
    def __init__(self, verbose=False):
        context = zmq.Context()
        self._socket = context.socket(zmq.PAIR)
        self._socket.connect("tcp://localhost:3004")

        self.verbose = verbose

        if self.verbose:
            print "Client Ready!"

        # Send a quick message to tell node process we are up and running
        self.send(json.dumps({
            'action': 'started',
            'command': 'status',
            'message': time.time()*1000.0
        }))

    def send(self, msg):
        """
        Sends a message to TCP server
        :param msg: str
            A string to send to node TCP server, could be a JSON dumps...
        :return: None
        """
        if self.verbose:
            print '<- out ' + msg
        self._socket.send(msg)
        return

    def recv(self):
        """
        Checks the ZeroMQ for data
        :return: str
            String of data
        """
        return self._socket.recv()




class P300(BioSignal):
    # CONSTRUCTORS--------------------------------------------------------------
    def __init__(self, sample_rate):
        # SUPERCLASS
        BioSignal.__init__(self)

        # ATTRIBUTES------------------------------------------------------------
        self.num_of_packets = 0
        # EOG data
        self.__eog_list__ = [[], [], []]
        self.__eog_list_filtered__ = [[], [], []]
        self.__peaks__ = [[],[]]

        self.__queue_length = 128

        # Board Characteristics
        self.sample_rate = sample_rate

        # Gestures
        #TODO: Encapsulate into classes
        self.left_gaze = False
        self.right_gaze = False
        self.up_gaze = False
        self.down_gaze = False
        self.blink = False

        self.gesture_list = [[0,0]]



    # FACTORY METHODS-----------------------------------------------------------
    # GETTERS, SETTERS----------------------------------------------------------

    # TODO: make thread-safe
    # METHODS-------------------------------------------------------------------
    def update(self, sample):
        self.num_of_packets += 1

        # self.__eog_list__[0].pop(0)
        # self.__eog_list__[1].pop(0)
        # self.__eog_list__[2].pop(0)

        # Append data to EOG list
        # TODO: encapsulate EOG List into something that reads more nicely
        # could use a dictionary
        self.__eog_list__[0].append(float(sample[0]))
        self.__eog_list__[1].append((float(sample[2]) - float(sample[1])) /
                                    1000000.0)
        self.__eog_list__[2].append((float(sample[4]) - float(sample[3])) /
                                    1000000.0)

        # print(sample)
        if self.num_of_packets > 300:
            self.__eog_list__[0].pop(0)
            self.__eog_list__[1].pop(0)
            self.__eog_list__[2].pop(0)


    def process(self):


        if self.num_of_packets >= self.__queue_length:

            # Apply bandpass filter
            self.__eog_list_filtered__[1] = self.bandpass\
                (self.__eog_list__[1])
            self.__eog_list_filtered__[2] = self.bandpass\
                (self.__eog_list__[2])

            # Apply smoothing
            self.__eog_list_filtered__[1] = self.smooth \
                (self.__eog_list__[1])
            self.__eog_list_filtered__[2] = self.smooth \
                (self.__eog_list__[2])

            # Find peaks
            self.__peaks__[0] = self.find_peaks(self.__eog_list_filtered__[1],
                                                self.sample_rate)
            self.__peaks__[1] = self.find_peaks(self.__eog_list_filtered__[2],
                                                self.sample_rate)
            print(self.__peaks__)
            # Find gesture
            # self.id_gestures()
            # self.gesture_graph()
            #
            # self.left_gaze = False
            # self.right_gaze = False
            # self.up_gaze = False
            # self.down_gaze = False
            # self.blink = False

    # def update_eog(self):
    #     '''
    #     :return: None
    #     '''
    #     # OPEN CSV AND READ LINES
    #     with open('./../packets.csv', 'rb') as ecg_file:
    #         ecg_reader = csv.reader(ecg_file, delimiter=self.COMMA_DELIMITER)
    #
    #         # INTERPRET EACH LINE
    #         for row in ecg_reader:
    #             # Extract data needed
    #             data_to_add = []
    #             data_to_add.append(row[0])
    #             data_to_add.append(float(row[3]) - float(row[2]))  # Einthoven
    #             # Append to ECG list
    #             self.__eog_list__.append(data_to_add)


    # HELPER FUNCTIONS----------------------------------------------------------
    def bandpass(self, data):
        ret_list = []
        data = []

        # Give enough data points to filter properly
        if len(data) >= self.__queue_length:

            # Calculate order of filter
            order = int(0.3 * self.sample_rate)

            # Apply filters
            filtered_data, _, _ = st.filter_signal(signal=data,
                                                   ftype='FIR',
                                                   band='bandpass',
                                                   order=order,
                                                   frequency=[0.1, 50],
                                                   sampling_rate=
                                                   self.sample_rate)

            ret_list = filtered_data

        else:
            ret_list = data

        return ret_list

    def smooth(self, data):
        sm_size = int(0.08 * self.sample_rate)

        smoothed_data, _ = st.smoother(signal=data,
                                           kernel='hamming',
                                           size=sm_size, mirror=True)

        return smoothed_data

    def find_peaks_helper(self, data, sampling_rate):
        peaks = []
        num_stds = 1.99

        count = 0
        while count < len(data):

            # Calculate Window
            if (count + (int)(num_stds * sampling_rate)) < len(data):
                window = data[count:
                (count + (int)(num_stds * sampling_rate) + 1)]
            else:
                window = data[count:len(data)]

            mean = window.mean()
            stdev = window.std()

            for val in window:
                if abs(val) > num_stds * stdev:
                    peaks.append(100)
                else:
                    peaks.append(0)

            count += (int)(num_stds * sampling_rate) + 1

        return peaks

    def find_peaks(self, data, sampling_rate):
        # VARS
        peaks = []
        peaks_pos = []
        peaks_neg = []
        data_pos = []
        data_neg = []

        # SEPARATE POS FROM NEG
        for val in data:
            if val < 0:
                data_neg.append(val)
                data_pos.append(0)
            else:
                data_pos.append(val)
                data_neg.append(0)

        # FIND PEAKS IN EACH
        peaks_neg = self.find_peaks_helper(np.array(data_neg, float),
                                        sampling_rate)
        peaks_pos = self.find_peaks_helper(np.array(data_pos, float),
                                        sampling_rate)

        # RECOMBINE
        for i in range(0, len(data)):
            if peaks_neg[i] == 100:
                peaks.append(-100)
            elif peaks_pos[i] == 100:
                peaks.append(100)
            else:
                peaks.append(0)

        return peaks

    def id_gestures(self):
        if(self.__eog_list__[0] > 300):
            for i in range(0, len(self.__peaks__[0])):
                if(self.__peaks__[0] == -100 and self.__peaks__[1] == 100):
                    self.blink = True
                    return
                elif(self.__peaks__[1] == 100):
                    self.left_gaze = True
                    return
                elif(self.__peaks__[1] == -100):
                    self.right_gaze = True
                    return
                elif(self.__peaks__[0] == 100):
                    self.up_gaze = True
                    return
                elif(self.__peaks__[0] == -100):
                    self.down_gaze = True
                    return

    def gesture_graph(self):

        curr_gesture = self.gesture_list[-1][0] + 1

        if(self.left_gaze == True):
            self.gesture_list.append([curr_gesture, 1])

        elif (self.right_gaze == True):
            self.gesture_list.append([curr_gesture, 2])

        elif (self.up_gaze == True):
            self.gesture_list.append([curr_gesture, 3])

        elif (self.down_gaze == True):
            self.gesture_list.append([curr_gesture, 4])

        elif (self.blink == True):
            self.gesture_list.append([curr_gesture, 5])

        else:
            self.gesture_list.append([curr_gesture, 0])
def process(biosignal):
    # stop = False
    # while not stop:
    #     biosignal.process()
    #
    #     if biosignal.is_stop():
    #         stop = True
    exit = False

    while not exit:
        if not biosignal.is_stop():
            biosignal.process()
        if biosignal.is_exit():
            exit = True

def main(argv):
    nb_chan = 8
    verbose = True
    Biosignal = P300(256)
    # Create a new python interface.
    interface = Interface(verbose=verbose)
    process_thread = threading.Thread(target=process, args=[Biosignal])

    num = 0
    while True:
        sample = interface.recv()
        Biosignal.update(sample)
        if num = 0:
            process_thread.start()
            num += 1

if __name__ == '__main__':
    main(sys.argv[1:])
