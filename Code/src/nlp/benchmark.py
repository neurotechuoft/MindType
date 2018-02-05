from complete import autocomplete
import time
import codecs
import pandas as pd

def benchmark(file: str) -> float:
    """
    Benchmark the average time it takes to find the next word from a file
    :param file: A file that lists the words to complete, separated by newline
    :return: the average time to predict the words
    """
    with open(file) as f:
        content = f.readlines()

    time_total = [time_wrapper(x) for x in content]

    return (sum(time_total) * 1.0) / len(time_total)


def time_wrapper(word: str) -> float:
    """
    A wrapper for the autocomplete function, to make it time each call
    :param word: A word to complete
    :return: time it takes to complete the word
    """
    start = time.time()
    autocomplete(word)
    return (time.time() - start) * 1000.0

def performance_test():
    # Performance Tests
    with codecs.open('/Users/ouutsuyuki/PycharmProjects/random/test_data_w2', "r", encoding='utf-8',
                     errors='ignore')  as source:

        testdata = pd.read_table(source, names=["freq", "first", "second"])

    # Intrinstic Test 1: 2nd word prediction based on first word input
    c1 = 0
    for i in range(1, len(testdata)):
        #a1, a2, a3 = autocomplete(testdata["first"][i] + ' ')
        #result =
        if autocomplete(testdata["first"][i] + ' ') == testdata["second"][i]:
            c1 = c1 + 1
    print('Test1: Prediction accuracy = ', c1 / len(testdata))

    '''
    Usage: python complete.py phrase_to_complete
    Test1: Prediction accuracy =  0.05392156862745098
    '''

    # Test 2: Prediction of Completing a word given increasing amount of alphabet input
    c2 = 0
    n = 0  # Number of comparision
    # for i in range(1, len(testdata)):
    for i in range(10):
        for j in range(len(testdata["first"][i])):
            n += 1
            if autocomplete(testdata["first"][i][:j]) == testdata["first"][i]:
                c2 = c2 + 1

        for k in range(len(testdata["second"][i])):
            n += 1
            if autocomplete(testdata["second"][i][:k]) == testdata["second"][i]:
                c2 = c2 + 1

    print('Test2: Prediction accuracy = ', c2 / n)

    '''
        Test2: Prediction accuracy =  0.2661290322580645 for 10 sets of words
    '''

    return (c1 / len(testdata), c2 / n)


if __name__ == "__main__":
    print(benchmark("test.txt"))
