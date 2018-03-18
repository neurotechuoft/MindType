from biosignals.biosignal import BioSignal
import biosppy
import numpy as np


class RealtimeBiosignal(BioSignal):
    def __init__(self):
        super(RealtimeBiosignal, self).__init__()

        # CONSTANTS-------------------------------------------------------------
        # CSV
        self.COMMA_DELIMITER = ","

        self.data = []

    # GETTERS, SETTERS----------------------------------------------------------

    # METHODS-------------------------------------------------------------------
    def update(self, sample):
        BioSignal.update(self, sample)
        print("PrintBiosignal received " + str(sample))
        if not self.__paused__:
            self.data.append(sample)

    def process(self):
        if len(self.data) > 12 and not self.__paused__:
            c4 = np.array([])
            c3 = np.array([])
            for i in range(12):
                row = self.data.pop()
                np.append(c3, [float(row[4])])
                np.append(c4, [float(row[5])])
            
            analyze_data = c3
            # analyze_data = np.subtract(analyze_data, np.full((len(analyze_data)), analyze_data.item(0)))
            analyze_data = np.subtract(analyze_data, np.full((len(analyze_data)), np.mean(c3)))

            # cleaned_data = bandpass(highpass(analyze_data, sample_rate, 2), sample_rate, 2.0, 50.0)
            cleaned_data = bandpass(analyze_data, sample_rate, 2.0, 50.0)

            mu = bandpass(cleaned_data, 256.0, 7.0, 13.0)

            mu_power = scale(np.reshape(fill_bandpower(mu, time, sample_rate, 7.0, 13.0), (-1, 1))).ravel()
    
    
    # HELPERS FUNCTIONS---------------------------------------------------------
    def relative_mu_threshold():
    
    def classify(mu_power, threshold):
        # returns 0 is off, returns 1 if on
        return (m_power >= threshold)
    
    def bandpass(data, sample_rate, low_freq, high_freq):
        # Calculate order of filter
        order = int(0.3 * sample_rate)

        # Apply filters
        filtered_data, _, _ = biosppy.tools.filter_signal(signal=data,
                                                          ftype='FIR',
                                                          band='bandpass',
                                                          order=order,
                                                          frequency=[low_freq,
                                                                     high_freq],
                                                          sampling_rate=
                                                          sample_rate)

        return filtered_data
    
    def fill_bandpower(data, time, sample_rate, low_freq, high_freq):
        mu_power_c3 = np.array([])
        c3_packet = np.array([])
        curr_gesture = gesture.item(0)
        for i in range(0, len(time)):
            # Calculate bandpower for packet, and reset packet
            if gesture.item(i) != curr_gesture or i == len(time) - 1:
                power = bandpower(c3_packet, sample_rate, low_freq, high_freq)
                for sample in c3_packet:
                    mu_power_c3 = np.append(mu_power_c3, power)
                curr_gesture = gesture.item(i)
                c3_packet = np.array([data.item(i)])
            else:
                # store all vals of the same gesture
                c3_packet = np.append(c3_packet, data.item(i))
        return np.append(mu_power_c3, mu_power_c3.item(-1))
