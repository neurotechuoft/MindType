import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter, butter
from math import sin


def butter_bandpass(lowcut, highcut, order=5):
    nyq = 0.5 * 250
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, order=5):
    b, a = butter_bandpass(lowcut, highcut, order=order)
    filtered_data = lfilter(b, a, data)
    return filtered_data

if __name__ == '__main__':

    data = []
    # INTERPRET EACH LINE
    #with open('2016-8-23_17-52-48.csv', 'rb') as ecg_file:
    with open('OpenBCI-RAW-aaron_ecg_1.csv', 'rb') as ecg_file:
        ecg_reader = csv.reader(ecg_file, delimiter=',')

        counter = 0

        for row in ecg_reader:
            #print(row)
            #print("\n")

            data.append(float(str(row[1])))
            counter+= 1

    Fs = 250.0  # sampling rate
    Ts = 1.0 / Fs  # sampling interval
    t = []

    for i in range(0, len(data)):
        t.append(i*Ts)

    ff = 256  # frequency of the signal

    filtered_data = butter_bandpass_filter(data, 0, 49)



    plt.plot(t, filtered_data, 'r')
    #plt.plot(t, data, 'b')
    plt.xlabel("Time")
    plt.ylabel("Amplitude (V)")

    plt.show()