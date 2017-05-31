import csv
from biosppy.signals import tools as st
import matplotlib.pyplot as plt
import numpy as np
import uinput
import time

def find_peaks_helper(data, sampling_rate):
    peaks = []
    num_stds = 1.99

    count = 0
    while count < len(data):

        # Calculate Window
        if (count + (int)(num_stds*sampling_rate)) < len(data):
            window = data[count:
            (count + (int)(num_stds*sampling_rate) + 1)]
        else:
            window = data[count:len(data)]

        mean = window.mean()
        stdev = window.std()

        for val in window:
            if abs(val) > num_stds * stdev:
                peaks.append(100)
            else:
                peaks.append(0)

        count += (int)(num_stds*sampling_rate) + 1

    return peaks

def find_peaks(data, sampling_rate):
    # VARS
    peaks = []
    peaks_pos = []
    peaks_neg = []
    data_pos = []
    data_neg = []

    # SEPARATE POS FROM NEG
    for val in data:
        if val < 0:
            data_neg.append(val)
            data_pos.append(0)
        else:
            data_pos.append(val)
            data_neg.append(0)

    # FIND PEAKS IN EACH
    peaks_neg = find_peaks_helper(np.array(data_neg, float), sampling_rate)
    peaks_pos = find_peaks_helper(np.array(data_pos, float), sampling_rate)

    # RECOMBINE
    for i in range(0, len(data)):
        if peaks_neg[i] == 100:
            peaks.append(-100)
        elif peaks_pos[i] == 100:
            peaks.append(100)
        else:
            peaks.append(0)


    return peaks

if __name__ == '__main__':

    data_ch1 = []
    data_ch2 = []
    # INTERPRET EACH LINE
    #with open('2016-8-23_17-52-48.csv', 'rb') as ecg_file:
    # with open('OpenBCI-RAW-aaron_ecg_1.csv', 'rb') as ecg_file:
    with open('./../../../../Data-Repository/EOG-Data/Nov-15-2016/CSV'
              '/OpenThenCenterRightCenterLeftCycles.csv', 'rb') as \
            ecg_file:

        ecg_reader = csv.reader(ecg_file, delimiter=',')

        counter = 0

        for row in ecg_reader:
            #print(row)
            #print("\n")

            data_ch1.append(float(str(row[0])))
            data_ch2.append(float(str(row[1])))

            counter+= 1

    data_ch1_arr = np.array(data_ch1)
    data_ch2_arr = np.array(data_ch2)


    sampling_rate = 960.0  # sampling rate
    Ts = 1.0 / sampling_rate  # sampling interval
    sm_size = int(0.08 * sampling_rate) #
    t = []
    eye_left = []

    for i in range(0, len(data_ch1)):
        t.append(i*Ts)

    order = int(0.3 * sampling_rate)

    # Filter Data
    filtered_data_ch1, _, _ = st.filter_signal(signal=data_ch1_arr,
                                               ftype='FIR',
                                               band='bandpass',
                                               order=order,
                                               frequency=[2, 50],
                                               sampling_rate=sampling_rate)

    filtered_data_ch2, _, _ = st.filter_signal(signal=data_ch2_arr,
                                               ftype='FIR',
                                               band='bandpass',
                                               order=order,
                                               frequency=[2, 50],
                                               sampling_rate=sampling_rate)


    # Smooth
    filtered_data_ch1, _ = st.smoother(signal=filtered_data_ch1,
                                       kernel='hamming',
                                       size=sm_size, mirror=True)

    filtered_data_ch2, _ = st.smoother(signal=filtered_data_ch2,
                                       kernel='hamming',
                                       size=sm_size, mirror=True)

    # Peaks

    peaks_ch1 = find_peaks(filtered_data_ch1, sampling_rate)

    peaks_ch2 = find_peaks(filtered_data_ch2, sampling_rate)


    for i in range(0, len(peaks_ch1)):
        peak1 = -5
        peak2 = -5

        if (peaks_ch1[i] == -100 and peaks_ch2[i] == 100):
            print("blink\n")
        elif (peaks_ch2[i] == 100):
            print("left_gaze\n")
        elif (peaks_ch2[i] == -100):
            print("right_gaze\n")
        elif (peaks_ch1[i] == 100):
            print("up_gaze\n")
        elif (peaks_ch1[i] == -100):
            print("down_gaze\n")



    # print(filtered_data)
    # print("len of t is")
    # print(len(t))
    # print("\n")
    #
    # print("len of max_peaks is")
    # print(len(peaks))
    # print("\n")

    plt.plot(t, filtered_data_ch1, 'r')
    plt.plot(t, peaks_ch1, 'g')
    # plt.plot(t, filtered_data_ch2, 'b')
    # plt.plot(t, peaks_ch2, 'g')
    # plt.plot(t, data, 'b')
    plt.xlabel("Time")
    plt.ylabel("Amplitude (V)")

    plt.show()

    # device = uinput.Device([
    #     uinput.BTN_LEFT,
    #     uinput.BTN_RIGHT,
    #     uinput.REL_X,
    #     uinput.REL_Y,
    # ])
    #
    # for i in filtered_data:
    #     device.emit(uinput.REL_X, (int) (i*10))
    #     device.emit(uinput.REL_Y, (int) (i*10))
    #     time.sleep(0.1)