from stream_rt import *
import threading


class RTAnalysis(object):
    """ Adapted from rteeg.rteeg.analysis.Loopanalysis (due to PyQt5 error with Python2.7 in original)
    Class to loop analysis of EEG data every time the markers stream notifies the end of the trial
    Parameters
    ----------
    m_stream : Marker Stream
       The marker stream to which you are connected.
    eeg_stream : MuseEEGStream
       The eeg stream to which you are connected.
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
        """
        print("Analysis started")
        sleep_time = 60  # Time to sleep between queries.

        while not self._kill_signal.is_set():
            # count/ or some marker to indicate end of trial
            # TODO: clear up what the trigger for analysis will be, including sleep time
            trial_end = 1
            # when marker data indicates the end of the trial,
            if trial_end:
                # Make an MNE epoch, decim = keep every nth sample
                trial = eeg_stream.make_epochs(m_stream, data_duration, tmin=0.0, tmax=0.750)
                # get input to classifier
                classifier_input = trial.get_data()
                # TODO: associate markers with classifier input array
                c = np.array([classifier_input])
                # print('size of classifier-input: {}' .format(c.shape))
                # print(c[0, 0, 1, :])
            else:
                print('kill signal')

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