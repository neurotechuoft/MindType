import csv
from biosppy.signals import tools as st
from biosignals.biosignal import BioSignal
from scipy.signal import butter, lfilter, resample
from scipy.ndimage.filters import laplace
import numpy as np
import mne

class MMC(BioSignal):

    def __init__(self, sample_rate):
        BioSignal.__init__(self)
        self.sample_rate = sample_rate
        self.__queue_length = 128
        self.eeg_data = [[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

    def update(self, sample):
        pass

    def process(self):

        # Data Processing (Edelman et al, 2014)
        # Downsampling to 100 hz.
        downsampled = downsample(self, self.eeg_data)

        # Filtering the with FIR bandpass filter between 5hz and 30hz
        bandpassed = bandpass(self, downsampled)

        # Surface laplacian is then applied to enhance focal activity
        # surrounding each electrode (Edelman et al, 2014)
        filtered = scipy.ndimage.filters.laplace(bandpassed)

        pass


    # Benedetta:
    # mne is a library that needs to be added. I included it in the conda environment I am using for Neurotech.
    # The python version required to run mne is 2.7

    # Minimum Norm Estimate
    # Measure in magnetoencephalography
    # Further info https://martinos.org/mne/stable/manual/source_localization/inverse.html
    # From paper the equation is x = (A.T * A + lambda * I)^-1 A.T b
    # from documentation x seems to be an array of P strengths of sources located on the cortical mantle
    # b is a 1xN array, where N is the number of channels recording EEG data
    def mne(self):







    def bandpass(self, data):

        ret_list = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        for i in length(data):
        # Give enough data points to filter properly
            if len(data[i]) >= self.__queue_length:

            # Calculate order of filter
                order = int(0.3 * self.sample_rate)

                # Apply filters
                filtered_data, _, _ = st.filter_signal(signal=data,
                                                       ftype='FIR',
                                                       band='bandpass',
                                                       order=order,
                                                       frequency=[5, 30],
                                                       sampling_rate=
                                                       self.sample_rate)

                ret_list[i] = filtered_data

            else:
                ret_list[i] = data[i]

        return ret_list

    def downsample(self, data):

        downsampled= [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]];

        for i in length(data):
            secs = len(data[i])/256 # Number of seconds in signal X
            samps = secs*100     # Number of samples to downsample
            downsampled[i] = scipy.signal.resample(data[i], samps)
        return downsampled
