from stream_rt import *
import threading
import time


class RTAnalysis(object):
    """ Adapted from rteeg.rteeg.analysis.Loopanalysis (due to PyQt5 error with Python2.7 in original)
    Class to loop analysis of EEG data every time the markers stream notifies the end of the trial
    Parameters
    ----------
    m_stream : Marker Stream
       The marker stream to which you are connected.
    eeg_stream : MuseEEGStream
       The eeg stream to which you are connected.
    data_duration : float
        The length of time that will be used to create all epochs for prediction (i.e. 12 flashes --> 3.4s)
    """

    def __init__(self, m_stream, eeg_stream, data_duration):
        if not isinstance(m_stream, MarkerStream):
            raise TypeError("Stream must be type `MuseEEGStream`. {} "
                            "was passed.".format(type(m_stream)))
        print("Analysis object created")
        self.m_stream = m_stream
        self.eeg_stream = eeg_stream
        # data_duration should be (number of flashes * (duration of each flash + in-between time)) + 1s
        self.data_duration = data_duration

        self.running = False
        self._kill_signal = threading.Event()
        self.classifier_input = None
        # make stream inlet
        # info = pylsl.StreamInfo('MLinput', '', 1, 0, 'int32', 'myuidw43536')
        # next make an outlet
        # outlet = pylsl.StreamOutlet(info)
        # if outlet:
        # print("ML stream established")

    def _loop_analysis(self):
        """Call a function every time the marker stream gives the signal"""
        self._loop_worker(self.m_stream, self.eeg_stream, self.data_duration)

    def _loop_worker(self, m_stream, eeg_stream, data_duration):
        """Adapted from rteeg.rteeg.analysis._loop_worker
        Parameters
        ----------
        m_stream: MarkerStream
            Stream of EEG data or event markers.
        eeg_stream: MuseEEGStream
        data_duration : float
            The length of time that will be used to create all epochs for prediction (i.e. 12 flashes --> 3.4s)
        """
        sleep_time = 0.01  # Time to sleep between queries.
        train = 1

        while not self._kill_signal.is_set():
            # when items exist in the marker analysis queue
            if not m_stream.analyze.empty():
                print('Began analyzing data...')

                # get last eeg sample for analysis of the trial (0.02% second tolerance to always capture 1st event)
                ts = m_stream.remove_analysis()
                tmp = np.array(eeg_stream.data)
                end_index = int((np.abs(tmp[:, -1] - ts)).argmin() + 1 / (1 / eeg_stream.info['sfreq']))

                # ensure enough there is enough eeg data before analyzing; wait if there isn't
                while len(eeg_stream.data) < end_index:
                    time.sleep(sleep_time)

                # Make an MNE epoch from channels 0-3 (EEG), decim = keep every nth sample
                epochs, identities, targets = eeg_stream.make_epochs(m_stream, end_index, data_duration,
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
                if train:
                    train_data = zip(targets, data)

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