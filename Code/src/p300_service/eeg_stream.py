"""Adapted LSLSStream object from Real Time EEG repo found here: https://github.com/kaczmarj/rteeg.
Contains classes which update their EEG and marker/stimulus data in real time over lsl. Pre-processes data and makes it
available for analysis.
"""
import base_stream
import numpy as np
import pylsl
from mne import create_info, Epochs, io


def look_for_eeg_stream():
    """returns an inlet of the first eeg stream outlet found."""
    print("looking for an EEG stream...")
    streams = pylsl.resolve_byprop('type', 'EEG', timeout=30)
    if len(streams) == 0:
        raise (RuntimeError, "Can't find EEG stream")
    print("Start acquiring data")
    eeg_inlet = pylsl.StreamInlet(streams[0], max_chunklen=1)

    return eeg_inlet


def look_for_markers_stream():
    """returns an inlet for the first markers stream outlet if found."""
    print("looking for a Markers stream")
    marker_streams = pylsl.resolve_byprop('name', 'Markers', timeout=2)

    if marker_streams:
        marker_inlet = pylsl.StreamInlet(marker_streams[0])
        return marker_inlet
    else:
        print("Can't find Markers stream")
        return 0


def raw_filter(raw, low_f, high_f, picks):
    """Filters data with a bandpass 4th order butterworth filter.
    Args:
        raw: mne.io.RawArray.
        low_f: lower frequency cutoff.
        high_f: upper frequency cutoff.
        picks: list; contains channel indexes.
    """
    raw.filter(low_f, high_f, method='iir', picks=picks)


def notch_filter(raw, frequencies, picks):
    """Notch filter.
    Narrow filter that removes specific frequencies.
    Args:
        raw: mne.io.RawArray.
        frequencies: array, contains notch frequencies.
        picks: list, contains channel indexes.
    """
    raw.notch_filter(frequencies, picks=picks, filter_length='auto', phase='zero')


def plot_psd(raw, area_mode, picks):
    """Plot Power Spectral density.
    Args:
        raw: mne.io.RawArray.
        area_mode: string, 'std' or 'range'.
        picks: list, contains channel indexes.
    """
    raw.plot_psd(area_mode=area_mode, picks=picks, average=False)


def plot(raw, events, duration, n_channels, scalings):
    """Plot Power Spectral density
        Args:
            raw: mne.io.RawArray.
            events: from make_events.
            duration: float.
            n_channels: int.
            scalings: string; axes scaling.
        """
    raw.plot(events, duration=duration, n_channels=n_channels, scalings=scalings)


def make_events(data, marker_stream, marker_end, trial_num, event_duration=0):
    """Create array of markers.
    This function creates an array of markers that is compatible with mne.Epochs. If no marker is found, returns ndarray
    indicating that one event occurred at the same time as the first sample of the EEG data, effectively making an
    Epochs object out of all of the data (until tmax of mne.Epochs).
    Args:
        data: ndarray; EEG data in the shape (n_channels + timestamp, n_samples).
        marker_stream: MarkerStream; Stream of marker data.
        marker_end: index of the laster marker in a set of trials
        trial_num: number of trials in a set
        event_duration: int (defaults to 0); duration of each event marker in seconds. This is not epoch duration.
    Returns:
        markers: ndarray (n_events x 3); details the occurence index in main data, duration, and target.
        targets: list containing target values for training; i.e. 0 or 1.
    """
    # Get the markers between two times.
    lower_time_limit = float(data[-1, 0])
    upper_time_limit = float(data[-1, -1])

    # Copy markers into a Numpy ndarray.
    tmp = np.array([row[:] for row in marker_stream.data[(marker_end - trial_num):marker_end]
                    if upper_time_limit >= float(row[-1]) >= lower_time_limit])

    # Pre-allocate array for speed.
    markers = np.zeros(shape=(tmp.shape[0], 3), dtype='int32')
    targets = np.zeros(shape=(tmp.shape[0], 1))

    # If there is at least one marker:
    if tmp.shape[0] > 0:
        for marker_index, (marker_int, timestamp) in enumerate(tmp):
            # Get the index where this marker happened in the EEG data.
            eeg_index = (np.abs(data[-1, :] - float(timestamp))).argmin()

            # Add a row to the markers array.
            markers[marker_index, :] = eeg_index, event_duration, marker_int

            # event and target arrays
            targets[marker_index] = marker_int
        return markers, targets
    else:
        # Make empty markers, events, and targets array
        print("Creating empty markers array. No markers found.")
        return np.array([[0, 0, 0]]), np.array([[0]]), np.array([[0]])


class EEGStream(base_stream.BaseStream):
    """Connects to eeg and markers streams.
    Also contains method for creating epochs of data to be used for prediction and training.
    Attributes:
         key: channel positions (https://martinos.org/mne/stable/generated/mne.create_info.html#mne.create_info).
    """

    def __init__(self, thread_name, event_channel_name='P300', key='default'):
        super(EEGStream, self).__init__()
        self._eeg_unit = 'unknown'
        self.info = None
        self.thread_name = thread_name
        self.event_channel_name = event_channel_name
        self.key = key

    def lsl_connect(self):
        # Connect to LSL stream
        self.connect(self._connect, self.thread_name)

    def _connect(self):
        """Connects to EEG outlet and records streaming eeg data."""
        # Find eeg stream and markers stream
        self._eeg_stream = look_for_eeg_stream()
        self._active = True

        # get channel info.
        info = self._eeg_stream.info()

        # Get sampling frequency.
        sfreq = float(info.nominal_srate())

        # Get channel names.
        ch_names = []
        this_child = info.desc().child('channels').child('channel')
        for _ in range(info.channel_count()):
            ch_names.append(this_child.child_value('label'))
            this_child = this_child.next_sibling('channel')

        # Get the EEG measurement unit (e.g., microvolts).
        units = []
        this_child = info.desc().child('channels').child('channel')
        for _ in range(info.channel_count()):
            units.append(this_child.child('label').child_value('unit'))
            this_child = this_child.next_sibling('channel')
        if all(units):
            self._eeg_unit = units[0]
        else:
            print("Could not find EEG measurement unit.")

        # Add stimulus channel.
        ch_types = ['eeg' for _ in ch_names] + ['stim']
        ch_names.append(self.event_channel_name)

        # Create mne.Info object.
        try:
            self.info = create_info(ch_names=ch_names,
                                    sfreq=sfreq, ch_types=ch_types,
                                    montage=self.key)
        except ValueError:
            self.info = create_info(ch_names=ch_names,
                                    sfreq=sfreq, ch_types=ch_types,
                                    montage=None)
            print("Could not find montage for '{}'"
                  "".format(self.key))

        # Begin recording data in a loop
        self._record_data_indefinitely(self._eeg_stream)
        print('EEG data recording started.')

    def get_data(self, end_index, data_duration=None, scale=1):
        """Get recent EEG data of specified duration up to the specified ending index.
        Args:
            data_duration: int; window of data to output in seconds. If None, will return all of the EEG data.
            end_index: int; last index of data to be included in the copy.
            scale : int, float; value by which to multiply the EEG data. If None, attempts to scale values to volts.
        Returns:
            data : ndarray; array of EEG data with shape (n_channels + timestamp, n_samples).
        """
        if data_duration is None:
            data = np.array(self.copy_data()).T
            # Scale the data but not the timestamps.
            data[:-1, :] = np.multiply(data[:-1, :], scale)
        else:
            start_index = int(end_index - data_duration * self.info['sfreq'])
            data = np.array(self.copy_data(start_index, end_index)).T
            # Scale the data but not the timestamps.
            data[:-1, :] = np.multiply(data[:-1, :], scale)
        return data

    def make_epochs(self,
                    marker_stream,
                    end_index,
                    marker_end,
                    trial_num,
                    data_duration=None,
                    events=None,
                    filter_range: tuple=(0.5, 15),
                    event_duration=0, event_id=None, tmin=-0.2, tmax=1.0, baseline=(None, 0), picks=None, preload=False,
                    reject=None, flat=None, proj=True, decim=1, reject_tmin=None, reject_tmax=None, detrend=None,
                    on_missing='error', reject_by_annotation=False, verbose=None):
        """Create instance of mne.Epochs. If events are not supplied, this script must be connected to a Markers stream.
        Args:
            marker_stream: stream_rt.MarkerStream; stream of marker data.
            end_index: Last index in data that is included.
            marker_end: index of the last marker in a set of trials
            trial_num: number of trials in a set
            data_duration: int, float; duration of previous data to use. If data=10, returns instance of mne.Epochs of
                the previous 10 seconds of data.
            events: ndarray; array of events of the shape (n_events, 3).
            filter_range: tuple containing bandpass filter range in Hz
            everything else: Copy parameters from mne.Epochs.
        Returns:
            epochs: mne.Epochs; contains time segments of data_duration after stimuli for training and prediciton.
            identities: list containing the row/column that was flashed in order.
            targets: list containing target values for training; i.e. 0 or 1.
        """
        targets = []
        raw_data = self.get_data(end_index, data_duration=data_duration)
        if events is None:
            events, targets = make_events(raw_data, marker_stream, marker_end, trial_num, event_duration)

        # Replace timestamps with zeros.
        raw_data[-1, :] = 0

        # Create raw array
        raw = io.RawArray(raw_data, self.info)

        # Populate events in event channel
        raw.add_events(events, self.event_channel_name)
        event_id = {'Non-Target': 0, 'Target': 1}

        # Plot power spectral density
        # plot_psd(raw, 'std', picks=[0, 1, 2, 3])

        # Notch filter
        # notch_filter(raw, np.arange(50, 101, 50), picks=[0, 1, 2, 3])

        # bandpass filter the data between two ends of the filter_range
        raw_filter(raw, filter_range[0], filter_range[1], picks=[0, 1, 2, 3])

        # plot raw data for visualization/validation
        plot(raw, events, duration=data_duration, n_channels=5, scalings='auto')

        return Epochs(raw, events, event_id=event_id, tmin=tmin, tmax=tmax,
                      baseline=baseline, picks=picks,
                      preload=preload, reject=reject, flat=flat, proj=proj, decim=decim,
                      reject_tmin=reject_tmin,
                      reject_tmax=reject_tmax, detrend=detrend, on_missing=on_missing,
                      reject_by_annotation=reject_by_annotation,
                      verbose=verbose), targets
