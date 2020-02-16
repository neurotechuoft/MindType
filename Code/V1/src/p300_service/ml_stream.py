# import ml
import threading
import time
import numpy as np
from marker_stream import MarkerStream
from eeg_stream import EEGStream

import pickle

class MLStream(object):
    """Class to loop analysis of EEG data every time the markers stream notifies the end of the trial.
    Adapted from rteeg.rteeg.analysis.LoopAnalysis.
    Attributes:
        m_stream: MarkerStream; the marker stream to which you are connected.
        eeg_stream: MuseEEGStream; the eeg stream to which you are connected.
        test_path: string; path for classifier save file.
        analysis_time: time to analyze after an event in seconds
        event_time: event duration + in between event time in seconds
        train: Boolean; if true, will use live data to train. If false (default), will return predictions for stimuli.
        train_epochs: number of epochs (time segmeents after events) to collect before beginning training; only
            applicable when train is 'True'. For this to work well, ensure that this number is a multiple of the
            number of trials (events) that are being made into epochs and sent for training/prediction.
    """

    def __init__(self,
                 m_stream,
                 eeg_stream,
                 analysis_time=1.0,
                 event_time=0.2,
                 train_epochs=120):
        print("Analysis object created.")
        self._loop_analysis_thread = None
        self.m_stream = m_stream
        self.eeg_stream = eeg_stream
        self.analysis_time = analysis_time
        self.event_time = event_time
        self.running = False
        self._kill_signal = threading.Event()
        self.classifier_input = None
        self.train = None
        self.train_epochs = train_epochs

        self.train_number = 0
        self.data_duration = None

        # for sending to p300 server
        self.train_data = []
        self.predictions = []

        # extra time to ensure that all epochs are captured
        self.extra_time = 0.1


    def _loop_analysis(self):
        """Call a function every time the marker stream gives the signal"""
        self._loop_worker()

    def _loop_worker(self):
        """The main loop for performing real time analysis.
        Takes items from an analysis queue sequentially, forms mne epochs, and either uses the data for real time
        training or to predict the letter that was mind-typed.
        Structure is adapted from rteeg.rteeg.analysis._loop_worker.
        """
        sleep_time = 0.01  # Time to sleep between queries.

        while not self._kill_signal.is_set():
            # when items exist in the marker analysis queue
            if not self.m_stream.analyze.empty():
                marker_dict = self.m_stream.remove_analysis()
                epoch_id = marker_dict['epoch_id']
                num_events = int(marker_dict['num_events'])
                timestamp = float(marker_dict['timestamp'])
                marker_end = int(marker_dict['marker_end'])

                print(f'Began analyzing data for epoch {epoch_id}...')

                self.data_duration = num_events*self.event_time + self.analysis_time + self.extra_time
                tmp = np.array(self.eeg_stream.data)
                # get analysis_time seconds of data (in terms of the end_index) after the event
                end_index = int((np.abs(tmp[:, -1] - timestamp)).argmin()
                                + self.analysis_time * self.eeg_stream.info['sfreq']
                                + self.extra_time * self.eeg_stream.info['sfreq'])

                # ensure there is enough eeg data before analyzing; wait if there isn't
                while len(self.eeg_stream.data) < end_index:
                    time.sleep(sleep_time)

                # Make an MNE epoch from channels 0-3 (EEG), decim = keep every nth sample
                epochs, targets = self.eeg_stream.make_epochs(marker_stream=self.m_stream,
                                                              end_index=end_index,
                                                              marker_end=marker_end,
                                                              trial_num=num_events,
                                                              data_duration=self.data_duration,
                                                              picks=[0, 1, 2, 3],
                                                              tmin=0.0,
                                                              tmax=1,
                                                              decim=3)

                # get input to classifier
                data = np.array(epochs.get_data())
                # since the sample frequency is 256 Hz/3 = 85.33 Hz, indexes 8 and 64 is approximately 0.100 - 0.750 s
                data = data[:, :, 8:64]

                # If training classifier, send data to classifier with ground truth targets
                if self.train:

                    # Generate input and targets
                    i = np.array(data)
                    i = i[:, [0, 3], :]
                    i = i.tolist()

                    t = np.squeeze(np.array(targets))
                    t = t.tolist()

                    self.train_data.append({'uuid': epoch_id, 'train_data': i, 'train_targets':t})

                    # # Get accuracy of classifier based on test set
                    # # score = classifier.score(self.inputs_test, self.targets_test)
                    # score = ml.score(self.inputs_test, self.targets_test, classifier)
                    # print('Test Set Accuracy: {}%' .format(score*100))

                # else do a prediction
                else:
                    i = np.array(data)
                    i = i[:, [0, 3], :]
                    i = i.tolist()
                    self.predictions.append({'uuid': epoch_id, 'eeg_data': i})

            time.sleep(sleep_time)

    def start(self, train_mode):
        """Start the analysis loop."""
        self.train=train_mode
        if not self.running:
            self.running = True
            self._loop_analysis_thread = threading.Thread(target=self._loop_analysis, name="Analysis-loop")
            self._loop_analysis_thread.daemon = True
            self._loop_analysis_thread.start()
            print('Analysis loop started')
        else:
            print("Loop of analysis already running.")

    def stop(self):
        """Stop the analysis loop."""
        if self.running:
            self._kill_signal.set()
            self.running = False
            print("Loop of analysis stopped.")
        else:
            print("Loop of analysis not running. Nothing to stop.")

    def get_training_data(self):
        if len(self.train_data) > 0:
            return self.train_data.pop(0)

    def get_prediction_data(self):
        """Returns one set of prediction data if there are any, otherwise returns None"""
        if len(self.predictions) > 0:
            return self.predictions.pop(0)

    def get_mode(self):
        """ Returns true if in training mode, False if not """
        return self.train

    def set_mode(self, train_mode):
        self.train = train_mode
