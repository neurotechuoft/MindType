from stream_rt import *
import lda
import threading
import time


class RTAnalysis(object):
    """Class to loop analysis of EEG data every time the markers stream notifies the end of the trial.

    Adapted from rteeg.rteeg.analysis.LoopAnalysis.

    Attributes:
        m_stream: MarkerStream; the marker stream to which you are connected.
        eeg_stream: MuseEEGStream; the eeg stream to which you are connected.
        path: string; path for classifier save file.
        analysis_time: time to analyze after an event in seconds
        event_time: event duration + in between event time in seconds
        train: Boolean; if true, will use live data to train. If false (default), will return predictions for stimuli.
        train_epochs: number of epochs (time segmeents after events) to collect before beginning training; only
            applicable when train is 'True'. For this to work well, ensure that this number is a multiple of the
            number of trials (events) that are being made into epochs and sent for training/prediction.
    """

    def __init__(self, m_stream, eeg_stream, path, analysis_time=1.0, event_time=0.2, train='False',
                 train_epochs=120):
        if not isinstance(m_stream, MarkerStream):
            raise TypeError("Stream must be type `MuseEEGStream`. {} "
                            "was passed.".format(type(m_stream)))
        print("Analysis object created.")
        self.m_stream = m_stream
        self.eeg_stream = eeg_stream
        self.path = path
        self.analysis_time = analysis_time
        self.event_time = event_time
        self.running = False
        self._kill_signal = threading.Event()
        self.classifier_input = None
        self.train = train
        self.train_epochs = train_epochs
        self.train_number = 0
        self.train_data = []
        self.train_targets = []
        self.predictions = []
        self.data_duration = None

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
                print('Began analyzing data...')

                trial_num, ts, marker_end = self.m_stream.remove_analysis()
                self.data_duration = trial_num*self.event_time + self.analysis_time
                tmp = np.array(self.eeg_stream.data)
                # get analysis_time seconds of data (in terms of the end_index) after the event
                end_index = int((np.abs(tmp[:, -1] - ts)).argmin()
                                + self.analysis_time / (1 / self.eeg_stream.info['sfreq']))

                # ensure there is enough eeg data before analyzing; wait if there isn't
                while len(self.eeg_stream.data) < end_index:
                    time.sleep(sleep_time)

                # Make an MNE epoch from channels 0-3 (EEG), decim = keep every nth sample
                epochs, identities, targets = self.eeg_stream.make_epochs(self.m_stream, end_index, marker_end,
                                                                          trial_num, self.data_duration,
                                                                          picks=[0, 1, 2, 3], tmin=0.0, tmax=1, decim=3)
                # get input to classifier
                print('Formatting data for classifier...')
                data = np.array(epochs.get_data())
                # since the sample frequency is 220 Hz/3 = 73.33 Hz, indexes 8 and 55 is approximately 0.100 - 0.750 s
                data = data[:, :, 8:56]
                print('size of classifier-input: {}'.format(data.shape))
                print('size of identities: {}'.format(identities.shape))
                print('size of targets: {}'.format(targets.shape))

                # If training classifier, send data to classifier with ground truth targets
                if self.train:
                    self.train_number += data.shape[0]
                    if self.train_number < self.train_epochs:
                        self.train_data.extend(data)
                        self.train_targets.extend(targets)
                    else:
                        print('Training LDA classifier with {} epochs' .format(self.train_number))
                        i, t = lda.create_input_target(zip(self.train_targets, self.train_data))
                        classifier = lda.lda_train(i, t)
                        print("Finished training.")
                        lda.save(self.path, classifier)
                        self.train_number = 0
                # else do a prediction
                else:
                    classifier = lda.load(self.path)
                    i, t = lda.create_input_target(zip(targets, data))
                    prediction = lda.predict(i, classifier)
                    intermediate = 0
                    for index, item in enumerate(prediction):
                        # To account for the fact that every marker is associated with 4 channels, average the output
                        # of each channel (or apply specific weights to each channel, to possibly implement in future).
                        # Predictions for a single event based on 4 channels is appended to a list.
                        if (index + 1) % 4 == 0:
                            intermediate += item/4
                            self.predictions.append(intermediate)
                            intermediate = 0
                        else:
                            intermediate += item/4
            time.sleep(sleep_time)

    def start(self):
        """Start the analysis loop."""
        if not self.running:
            self.running = True
            self._loop_analysis_thread = threading.Thread(target=self._loop_analysis, name="Analysis-loop")
            self._loop_analysis_thread.daemon = True
            self._loop_analysis_thread.start()

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