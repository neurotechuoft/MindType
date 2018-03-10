"""Base class for recording streams of data. Adapted for Neurotech Mindtype"""
# Original Author: Jakub Kaczmarzyk <jakubk@mit.edu>
from __future__ import division, print_function, absolute_import
import threading


class BaseStream(object):
    """Base class for recording streams of data."""
    def __init__(self):
        self._active = False
        self._kill_signal = threading.Event()
        self.data = []

    def __del__(self):
        # Break out of the loop of data collection.
        self._kill_signal.set()

    def _update(self, row):
        self.data.append(row)

    def _record_data_indefinitely(self, inlet):
        """Record data to list, and correct for time differences between
        machines.

        Parameters
        ----------
        inlet : pylsl.StreamInlet
            The LabStreamingLayer inlet of data.
        """
        while not self._kill_signal.is_set():
            sample, timestamp = inlet.pull_sample()
            time_correction = inlet.time_correction()
            sample.append(timestamp + time_correction)
            self._update(sample)

    def connect(self, target, name):
        """Connect and record data in a separate thread.

        Parameters
        ----------
        target : callable
            The function to execute in the thread.
        name : str
            Name for the thread.

        Raises
        ------
        RuntimeError if attempting to connect more than once.
        """
        if self._active:
            raise RuntimeError("Stream already active.")
        else:
            self._thread = threading.Thread(target=target, name=name)
            self._thread.daemon = True
            self._thread.start()
            self._active = True

    def copy_data(self, start_index=None, end_index=None):
        """Return deep copy `self.data`.

        Parameters
        ----------
        start_index : int
        end_index : int
        Returns
        ----------
        array: list, items from start index to end index. By default, returns all items.
        """
        if start_index is None:
            # Make this a numpy array?
            tmp = self.data[:]  # Shallow copy.
            return [row[:] for row in tmp]  # Deep copy.
        else:
            current_max = len(self.data)
            if start_index > current_max:
                print("Start index {} was requested, but list only goes up to {}.".format(start_index, current_max))
            if end_index > current_max:
                print("end index {} was requested, but list only goes up to {}.".format(end_index, current_max))
            tmp = self.data[start_index:end_index + 1]  # Shallow copy.
            return [row[:] for row in tmp]  # Deep copy.