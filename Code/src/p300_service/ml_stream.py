import ml
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
                 classifier_path,
                 test_path,
                 analysis_time=1.0,
                 event_time=0.2,
                 train=False,
                 train_epochs=120,
                 get_test=False,
                 ):
        print("Analysis object created.")
        self._loop_analysis_thread = None
        self.m_stream = m_stream
        self.eeg_stream = eeg_stream
        self.classifier_path = classifier_path
        self.test_path = test_path
        self.analysis_time = analysis_time
        self.event_time = event_time
        self.running = False
        self._kill_signal = threading.Event()
        self.classifier_input = None
        self.train = train
        self.train_epochs = train_epochs
        self.get_test = get_test

        self.train_number = 0
        self.train_data = []
        self.train_targets = []
        self.data_duration = None

        # for sending to p300 server
        self.inputs = []
        self.targets = []
        self.predictions = []

        # extra time to ensure that all epochs are captured
        self.extra_time = 0.1

        # Load test data from pickle if we are not gathering test data
        if not get_test:
            self.test_set = ml.load_test_data(self.test_path)
            self.inputs_test = np.array([t[1] for t in self.test_set])
            self.targets_test = np.squeeze(np.array([t[0] for t in self.test_set]))
            self.inputs_test = self.inputs_test[:, [0, 3], :]

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

        # Load classifier if we want to make predictions
        if not self.train:
            classifier = ml.load(self.classifier_path)

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
                epochs, events, targets = self.eeg_stream.make_epochs(marker_stream=self.m_stream,
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
                    self.train_number += data.shape[0]
                    self.train_data.extend(data)
                    self.train_targets.extend(targets)

                    if self.train_number > self.train_epochs:

                        print('\n\n\n')
                        print('Training ml classifier with {} epochs'.format(self.train_number))
                        print('\n\n\n')

                        # package = list(zip(self.train_targets, self.train_data))

                        if self.get_test:
                            ml.save_test_data(self.test_path, package)
                            print("test set created!")
                            self._kill_signal.set()

                        else:
                            # Generate input and targets
                            # i = np.array([p[1] for p in package])
                            # i = i[:, [0, 3], :]
                            # t = np.squeeze(np.array([p[0] for p in package]))

                            i = np.array(self.train_data)
                            i = i[:, [0, 3], :]
                            t = np.squeeze(np.array(self.train_targets))

                            self.inputs.append(i)
                            self.target.append(t)

                            # # Note in Barachant's ipynb, 'erpcov_mdm' performed best. 'vect_lr' is the
                            # # universal one for EEG data.
                            # classifier = ml.ml_classifier(i, t, pipeline='vect_lr')
                            # print("Finished training.")
                            # ml.save(self.classifier_path, classifier)
                            # self.train_number = 0
                            #
                            # # Get accuracy of classifier based on test set
                            # # score = classifier.score(self.inputs_test, self.targets_test)
                            # score = ml.score(self.inputs_test, self.targets_test, classifier)
                            # print('Test Set Accuracy: {}%' .format(score*100))

                # else do a prediction
                else:
                    i = np.array(data)
                    i = i[:, [0, 3], :]
                    # predictions = ml.predict(i, classifier)

                    self.predictions.append({'epoch_id': epoch_id, 'prediction_data': i})

            time.sleep(sleep_time)

    def start(self):
        """Start the analysis loop."""
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
        if len(self.inputs) > 0 and len(self.targets) > 0:
            i = self.inputs.pop()
            t = self.targets.pop()
            return i, t

    def get_prediction_data(self):
        """Returns one set of prediction data if there are any, otherwise returns None"""
        if len(self.predictions) > 0:
            return self.predictions.pop(0)
