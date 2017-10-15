import numpy as np
import numpy.fft as fft
import matplotlib.pyplot as plt
import math
import GenerateToyData as td
import math

# Macros for tags' positions of data points corresponding to:
REST = 0
LEFT_HAND = 1
RIGHT_HAND = 2
BOTH = 3
# Macors for index of desired channel in data_set:
CHANNEL_3 = 2
CHANNEL_4 = 3
TAG_INDEX = 8
NO_FREQUENCY_BINS = 2

# Arrays to extract labelled data from data_set
rest_data = [[], []]
right_hand_data = [[], []]
left_hand_data = [[], []]
both_hand_data = [[], []]

def parse_dataset(data_set):
    '''
        Parse labelled data from channels 3 & 4 and add it to the global
        arrays specifid above to prepare for training
    '''
    for i in range(len(data_set[0])):
    #parsing the data set based on the tag for each data sample
        if data_set[TAG_INDEX][i] == REST:
            rest_data[0].append(data_set[CHANNEL_3][i])
            rest_data[1].append(data_set[CHANNEL_4][i])

        elif data_set[TAG_INDEX][i] == LEFT_HAND:
            left_hand_data[0].append(data_set[CHANNEL_3][i])
            left_hand_data[1].append(data_set[CHANNEL_4][i])

        elif data_set[TAG_INDEX][i] == RIGHT_HAND:
            right_hand_data[0].append(data_set[CHANNEL_3][i])
            right_hand_data[1].append(data_set[CHANNEL_4][i])

        elif data_set[TAG_INDEX][i] == BOTH:
            both_hand_data[0].append(data_set[CHANNEL_3][i])
            both_hand_data[1].append(data_set[CHANNEL_4][i])

    return 0


def find_mean_of_rest_data(data):
    ''' Find the mean of the rest data set '''
    #create array for the average sample in rest state
    mean_rest_data = [[0 for x in range(NO_FREQUENCY_BINS)] for y in range(2)]
    no_samples = int(math.ceil(len(data[0])/NO_FREQUENCY_BINS))
    for i in range(NO_FREQUENCY_BINS):
        mean_rest_data[0][i] = 0
        mean_rest_data[1][i] = 0


    #loop over entire array and add the voltages from the frequency bins
    index = 0
    for i in range(len(data[0])):

        mean_rest_data[0][index] += data[0][i]
        mean_rest_data[1][index] += data[1][i]
        index+=1

        if index == NO_FREQUENCY_BINS:
            index = 0

    for i in range(len(mean_rest_data[0])):
        mean_rest_data[0][i] = mean_rest_data[0][i]/no_samples
        mean_rest_data[1][i] = mean_rest_data[1][i]/no_samples

    return mean_rest_data


def find_most_frequent_highest_diff(mean_rest_data_freq, other_data_freq):
    ''' Compares the values of the two arrays element wise and
    returns the index (i.e. frequency bin) of the values (amplitudes)
    with highest absolute difference |x2 - x1| in the two data sets
    provided.
        Compares each sample with the mean_rest_data and returns
    the most frequent index with the highest differential
        Returns the most frequent index with highest differential among
    the samples.
    ''''
    max_diff_1, max_diff_2 = 0, 0
    max_index_1, max_index_2 = 0, 0
    highest_index1, highest_index2 = 0, 0
    tally_list = [[0 for x in range(NO_FREQUENCY_BINS)] for y in range(2)]

    # Look through all the nested lists within other_data_freq
    for i in range(len(other_data_freq)):

        # Look through the elements of each nested list
        for j in range(len(other_data_freq[i])):
            diff_1 = abs(mean_rest_data_freq[0][j] - other_data_freq[i][j])
            diff_2 = abs(mean_rest_data_freq[1][j] - other_data_freq[i][j])

            if diff_1 > max_diff_1:
                highest_index1 = i
                max_diff_1 = diff_1
            if diff_2 > max_diff_2:
                highest_index2 = i
                max_diff_2 = diff_2

    # Now the highest_index represent the index of the highest difference
    # between mean_rest_data_freq and the 'i'th nested list in other_data_freq
    tally_list[0][highest_index1] += 1
    tally_list[1][highest_index2] += 1

    max_diff_1, max_diff_2 = 0, 0
    highest_index1, highest_index2 = 0, 0

    max_val_1 = max(tally_list[0])
    max_val_2 = max(tally_list[1])

    for val in range(len(tally_list[0])):
        if tally_list[0][val] == max_val_1:
            max_index_1 = val
        if tally_list[1][val] == max_val_2:
            max_index_2 = val

    return [max_index_1, max_index_2]


'''
    Copied from here https://stackoverflow.com/questions/42414114/frequency-voltage-graph-from-eeg-data-fft-in-python
'''
def time_to_frequency(data):
   """Applying fast fourier transformation to the data to convert from time domain to
   frequency domain
   data must be 1d"""
   rest_data[0], rest_data[1] = np.fft.fft(rest_data[0]), np.fft.fft(rest_data[1])
   left_hand_data[0], left_hand_data[1] = np.fft.fft(left_hand_data[0]), np.fft.fft(left_hand_data[1])
   right_hand_data[0], right_hand_data[1] = np.fft.fft(right_hand_data[0]), np.fft.fft(right_hand_data[1])
   both_hand_data[0], both_hand_data[1] = np.fft.fft(both_hand_data[0]), np.fft.fft(both_hand_data[1])
   # Fs = 256.0 # sampling frequency
   # Ts = 1.0/Fs # period
   # t = np.arange(len(data)) / Fs # time axis for plotting
   #
   # n = len(data) # length of the signal
   # print "n: ", n
   # print "Ts: ", Ts
   # print "t: ", t
   # k = np.arange(n)
   # T = n/Fs # total time sampling
   # frq = k/T # two sides frequency range
   # frq = frq[range(int(n/2))]
   #
   # Y = np.fft.fft(data)
   # Y = Y[range(int(n/2))]
   #
   # fig, ax = plt.subplots(2, 1)
   # ax[0].plot(t,data)
   # ax[0].set_xlabel('Time')
   # ax[0].set_ylabel('Voltage')
   # ax[1].plot(frq,20*np.log10(abs(Y)),'r')
   # ax[1].set_xlabel('Freq (Hz)')
   #
   #
   #
   # plt.draw()
   # plt.show()
   #
   # fig.savefig("graph.png")
   #return np.fft.fft(data)

def main():
    # data = td.getHarmonicData(8, 1024)
    # print(data[:][:10])
    # parse_dataset(data)
    # print("Rest data: ")
    # print(rest_data[0])
    # print("Right data: ")
    # print(right_hand_data[0])
    #
    # fig, ax = plt.subplots(2, 1)
    # ax[0].plot(rest_data[0])
    # ax[1].plot(right_hand_data[0])
    #
    # plt.draw()
    # plt.show()


    #print "Data: \n", data
    #parse_dataset(data)
    #print "Rest data: \n", rest_data
    #print "Right hand: \n", right_hand_data
    #print "Left hand: \n", left_hand_data
    #print "Both hands: \n", both_hand_data
    #print "mean_rest_data: \n", find_mean_of_rest_data(rest_data)
    # data = td.getData(8, 8)
    #
    # print "Data: \n", data
    # parse_dataset(data)
    # print "Rest data: \n", rest_data
    # print "Right hand: \n", right_hand_data
    # print "Left hand: \n", left_hand_data
    # print "Both hands: \n", both_hand_data
    # print "mean_rest_data: \n", find_mean_of_rest_data(rest_data)
    #
    # print "most frequent highest differential: \n", find_most_frequent_highest_diff(find_mean_of_rest_data(rest_data), left_hand_data)

    #print "Right hand: \n", right_hand_data
    #print "Left hand: \n", left_hand_data
    #print "Both hands: \n", both_hand_data

    # print "Data: \n", data[0][:256]
    # rest_data_freq = time_to_frequency(data[0])
    #rest_data_freq = time_to_frequency(rest_data[0])
    #print "Rest data: \n", rest_data
    #print "Right hand: \n", right_hand_data
    #print "Left hand: \n", left_hand_data
    #print "Both hands: \n", both_hand_data

if __name__ == '__main__':
    main()
