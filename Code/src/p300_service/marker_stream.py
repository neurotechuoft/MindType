import base_stream
import pylsl
import queue
import json


def look_for_markers_stream():
    """returns an inlet for the first markers stream outlet if found."""
    print("looking for a Markers stream")
    streams = pylsl.resolve_byprop('name', 'Markers', timeout=2)
    if len(streams) == 0:
        raise (RuntimeError, "Can't find Markers stream")
    print("Start acquiring data")
    marker_inlet = pylsl.StreamInlet(streams[0])

    return marker_inlet


class MarkerStream(base_stream.BaseStream):
    """Class for marker stream object, with same structure as MuseEEGStream.
    Receives markers over lsl and places them in a queue for analysis.
    """

    def __init__(self, name='Marker_data'):
        super(MarkerStream, self).__init__()
        self.name = name
        self.analyze = queue.Queue()
        self.num_events = 0
        self.count = 0
        self.event_count_dict = {}

    def lsl_connect(self):
        # Connect to LSL stream
        self.connect(self._connect, self.name)

    def _connect(self):
        self._markers_stream = look_for_markers_stream()
        self._active = True

        # Begin recording data in a loop
        self._record_data_indefinitely(self._markers_stream)

    def add_analysis(self, item):
        self.analyze.put(item)

    def remove_analysis(self):
        item = self.analyze.get()
        return item

    def _record_data_indefinitely(self, inlet):
        """Record data to list and correct for time differences. Updates marker count to trigger analysis.
        The identifier is the letter/row/column/block/etc... that should be sent as an integer in the first channel.
        The timestamp of the marker should be sent in the second channel.
        Self.trial_num sets how many trials should be taken before analysis. The trial_num should be sent with marker
        data in channel 3 for the FIRST marker. A trial_num of zero means there is no change to the trial_num.
        Example: Keyboard has n trials. The first trial should send n, while the subsequent trials should send 0s. This
        tells the program that every n trials, it should queue n events for analysis. If the next set of trials contains
        m trials, the first marker of the new set should send m, with the subsequent trials sending 0s, etc...
        Args:
            inlet: pylsl.StreamInlet; the LabStreamingLayer inlet of data.
        """

        while not self._kill_signal.is_set():
            # Get marker data from inlet
            sample, timestamp = inlet.pull_sample()

            # sample = {t: (timestamp), event: (int), num_events: (int), epoch_id: (uuid)}
            t = sample[0]
            event = sample[1]
            target = sample[2]
            num_events = sample[3]
            epoch_id = sample[4]

            # create epoch entry if not previously recorded
            if epoch_id not in self.event_count_dict:
                self.event_count_dict[epoch_id] = 0

            # update marker data
            time_correction = inlet.time_correction()
            marker_sample = [event, target, timestamp + time_correction]
            self._update(marker_sample)

            # append count of epoch
            self.event_count_dict[epoch_id] += 1
            if self.event_count_dict[epoch_id] == num_events:
                # Get marker index of the last trial in that set
                marker_end = len(self.data)

                # If the set of trials finishes, queue last trial_num events for analysis (as a set of epochs)
                self.add_analysis({'epoch_id': epoch_id,
                                   'num_events': num_events,
                                   't': timestamp + time_correction,
                                   'marker_end': marker_end})
                print(f"Analysis queue updated with epoch: {epoch_id}")
