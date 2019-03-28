import base_stream
import pylsl
import queue


def look_for_markers_stream():
    """returns an inlet for the first markers stream outlet if found."""
    print("looking for a Markers stream")
    streams = pylsl.resolve_byprop('name', 'Markers', timeout=30)
    if len(streams) == 0:
        raise (RuntimeError, "Can't find Markers stream")
    print("Start acquiring data")
    marker_inlet = pylsl.StreamInlet(streams[0])

    return marker_inlet


class MarkerStream(base_stream.BaseStream):
    """Class for marker stream object, with same structure as MuseEEGStream.
    Receives markers over lsl and places them in a queue for analysis.
    """

    def __init__(self, thread_name='Marker_data'):
        super(MarkerStream, self).__init__()
        self.thread_name = thread_name
        self.analyze = queue.Queue()
        self.event_count_dict = {}

    def lsl_connect(self):
        # Connect to LSL stream
        self.connect(self._connect, self.thread_name)

    def _connect(self):
        self._markers_stream = look_for_markers_stream()
        self._active = True

        # Begin recording data in a loop
        self._record_data_indefinitely(self._markers_stream)

    def add_analysis(self, item):
        print('item added to queue!')
        self.analyze.put(item)

    def remove_analysis(self):
        item = self.analyze.get()
        return item

    def _record_data_indefinitely(self, inlet):
        """Record data to list and correct for time differences.
        This function recognizes samples that are in an array with the format:
            [
                [0]: timestamp: float - point in time (in seconds) at which the sample is published,
                [1]: event: int - identifier for the marker, i.e. a number that is mapped to a certain letter,
                [2]: target: int - boolean (0 or 1) that is used in training to mark the sample as a target value,
                [3]: num_events: int - number of events that are published in the epoch,
                [4]: epoch_id: uuid - unique identifier for a specific epoch
            ]

        Args:
            inlet: pylsl.StreamInlet; the LabStreamingLayer inlet of data.
        """

        while not self._kill_signal.is_set():
            # Get marker data from inlet
            sample, inlet_timestamp = inlet.pull_sample()

            # sample parameters
            timestamp = sample[0]
            event = sample[1]
            target = sample[2]
            num_events = sample[3]
            epoch_id = sample[4]

            # create epoch entry if not previously recorded
            if epoch_id not in self.event_count_dict:
                self.event_count_dict[epoch_id] = 0

            # update marker data
            marker_sample = [event, target, timestamp]
            self._update(marker_sample)

            # append count of epoch
            self.event_count_dict[epoch_id] += 1
            if self.event_count_dict[epoch_id] == int(num_events):
                # Get marker index of the last trial in that set
                marker_end = len(self.data)

                # If the set of trials finishes, queue last trial_num events for analysis (as a set of epochs)
                self.add_analysis({'epoch_id': epoch_id,
                                   'num_events': num_events,
                                   'timestamp': timestamp,
                                   'marker_end': marker_end})
                print(f"Analysis queue updated with epoch: {epoch_id}")
