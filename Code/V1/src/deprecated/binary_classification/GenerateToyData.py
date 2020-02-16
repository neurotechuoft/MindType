'''
    Generate toy EEG data to test TrainingAlgorithm
    Takes two arguments, first number of channels, second
    is number of samples.

    Result: nested list of sample lists, and last list is label data
'''
import random
import numpy as np

def getData(numChannels, numSamples):
    random.seed(2017)
    data = []
    # Fill voltage values:
    for channel in range(numChannels):
        data.append([])
        for value in range(numSamples):
            data[channel].append(random.randint(8, 16)/1.0)

    # Fill label values:
    data.append([])
    for value in range(numSamples):
        data[-1].append(random.randint(0,3))

    return data

def getHarmonicData(numbChannels, numSamples):
    data = []
    N = numSamples

    #n = np.arange(0, N)
    for n in range(numSamples):
        value = 0
        for frequency in range(20):
            if (frequency >= 8 and frequency <= 12):
                value += random.randint(50, 100) * np.sin(2*np.pi * frequency * n / numSamples)
            else:
                value += random.randint(0, 5) * np.sin(2*np.pi * frequency * n / numSamples)

        data.append(value)

    return data
    '''
    Delta = 2* np.pi / N
    n = np.arange(0, N)

    random.seed(2017)

    for channel in range(numbChannels):
        omega = 2 * np.pi / random.randint(0, numSamples)
        data.append(np.cos(omega * n) + np.cos((omega + 3*Delta) * n))

    data.append([])
    for sample in range(numSamples):
        data[-1].append(random.randint(0, 3))
    '''
    return data

def main():
    data = getData(2, 10)
    print "Array filled."
    print data

if __name__ == "__main__":
    main()
