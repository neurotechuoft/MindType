import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import rfft, irfft

def bandpass(data_list, min_hz, max_hz):

    fft_list = rfft(data_list)

    # Filter
    for i in range(len(fft_list)):
        if not (min_hz < i/2+1 < max_hz): fft_list[i] = 0

    result_vals = irfft(fft_list)

    return result_vals

def remove_freq_range(data_list, min_hz, max_hz):

    fft_list = rfft(data_list)

    # Filter
    for i in range(len(fft_list)):
        if (min_hz < i / 2 + 1 < max_hz): fft_list[i] = 0

    result_vals = irfft(fft_list)

    return result_vals


def remove_sixty_hz(data_list):
    return remove_freq_range(data_list, 59, 61)

if __name__ == '__main__':

    data = []
    # INTERPRET EACH LINE
    with open('OpenBCI-RAW-aaron_ecg_1.csv', 'rb') as ecg_file:
        ecg_reader = csv.reader(ecg_file, delimiter=',')

        counter = 0

        for row in ecg_reader:
            #print(row)
            #print("\n")
            if 400 < counter < 1200:
                data.append(float(str(row[1])))
            counter+= 1

    Fs = 256.0  # sampling rate
    Ts = 1.0 / Fs  # sampling interval
    t = []

    for i in range(0, len(data)):
        t.append(i*Ts)

    filtered_data = remove_sixty_hz(data)
    filtered_data = bandpass(filtered_data, 5, 50)

    # ff = 256  # frequency of the signal
    #
    # n = len(data)  # length of the signal
    # k = np.arange(n)
    # T = n / Fs
    # frq = k / T  # two sides frequency range
    # frq = frq[range(n / 2)]  # one side frequency range
    #
    # Y = np.fft.fft(data)/n  # fft computing and normalization
    # Y = Y[range(n / 2)]
    #
    #
    # plt.plot(frq, abs(Y), 'r')  # plotting the spectrum
    # plt.xlabel("Frequency")
    # plt.ylabel("Amplitude")

    plt.plot(t, filtered_data, 'r')  # plotting the spectrum
    plt.plot(t, data, 'b')
    plt.xlabel("Frequency")
    plt.ylabel("Amplitude")

    plt.show()