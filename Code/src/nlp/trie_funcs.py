import marisa_trie as marisa
import pandas as pd
import numpy as np
import codecs
import pickle
import sys

# TODO: Need to rewrite the file read. Right now it assumes that only one text file is used.
# The easiest way is to probably change load_data to combine 2 and 3-grams(and maybe more)

def autocomplete(start_word, data_path, triee=None):
    """
    Autocomplete a word by finding the most widely used n-gram starting with it.
    :param start_word: a word to autocomplete
    :param data_path: path to the word corpus
    :param triee: an optional argument in special case where a trie already exists, main purpose
    is debugging
    :return: a string with the autocompleted word
    """

    highest_freq = 0
    complete_word = ''

    # Get an appropriate trie
    if triee is None:
        triee = check_cache(data_path, start_word)

    # Iterate over the trie elements that start with the start_word
    # and store the one with the highest score.
    #for key, val in triee.items(start_word):
        # The values are singular tuples, where val[0] is the actual frequency
    #    if val[0] > highest_freq:
    #        highest_freq = val[0]
    #        complete_word = key


    # Iterate over the trie elements that start with the start_word
    # and store the top 3 most frequent words
    item = triee.items(start_word)

    complete_word = []
    complete_freq = []
    i = 0
    while len(item) > 0 and i < 3:
        highest_freq = 0
        for key, val in item:
            if val[0] > highest_freq:
                highest_freq = val[0]
                complete_word.append(key)
                complete_freq.append(val)
        item.remove((complete_word[-1],complete_freq[-1]))
        i += 1

    #if len(complete_word) == 0:
    #    return "Couldn't find autocomplete for \"{}\"".format(start_word)
    # For the case where the autocomplete predicts the next word

    results = []
    j = 0
    while j < len(complete_word) and j < 3:
        longer = complete_word[j].split(' ')
        if len(longer) > 1 and longer[-2] in start_word:
            # Ignore the first word, which was given as an input, return only the next one
            results.append(longer[-1])
        else:
            results.append(longer[0])
        j += 1

    while len(results) <= 3:
        results.append(start_word.split(' ')[0])
    return results[0], results[1], results[2]

    #if complete_word == '':
    #    return "Couldn't find autocomplete for \"{}\"".format(start_word)
    # For the case where the autocomplete predicts the next word
    #longer = complete_word.split(' ')
    #if len(longer) > 1 and longer[-2] in start_word:
        # Ignore the first word, which was given as an input, return only the next one
    #    return longer[-1]
    #return longer[0]


def check_cache(data_path, start_word):
    """
    Analyze the word and the cached tries. Choose the appropriate category for the word
    and create(and store)/load associated trie.
    :param data_path: path to the n-gram corpus
    :param start_word: word to complete
    :return: the loaded trie
    """
    try:
        short = open('./resources/short_trie.pkl', 'rb')
    except IOError:
        one_letter(data_path)
        short = open('./resources/short_trie.pkl', 'rb')
    try:
        long = open('./resources/trie.pkl', 'rb')
    except IOError:
        load_data(data_path)
        long = open('./resources/trie.pkl', 'rb')

    try:
        pop_trie = open('./resources/popular_trie.pkl', 'rb')
        pop_dict = open('./resources/dict.pkl', 'rb')
        popular_dict = pickle.load(pop_dict)

    except IOError:
        popular_trie(data_path)
        pop_trie = open('./resources/popular_trie.pkl', 'rb')
        pop_dict = open('./resources/dict.pkl', 'rb')
        popular_dict = pickle.load(pop_dict)

    if len(start_word) == 1:
        return pickle.load(short)
    if start_word in popular_dict:
        return pickle.load(pop_trie)

    return pickle.load(long)


def load_data(path_to_data, branch_limit=10000):
    """
    Load the longest version of the trie, containing most n-grams(limited by the branch_limit)
    :param path_to_data: path to the n-gram corpus
    :param branch_limit: the limit of children for each node of the trie. Default 10000
    :return: the trie, which also gets stored on the drive
    """

    with codecs.open(path_to_data, "r", encoding='utf-8', errors='ignore') as fdata:
        grams = pd.read_table(fdata, names=["freq", "first", "second"])

    grams = grams.sort_values(by='freq', ascending=False)

    # Limit the number of children for each node
    grams = grams.groupby("first").head(branch_limit)

    # The transformation from int to a singular tuple is required by the trie API
    grams['freq'] = grams['freq'].apply(lambda x: (x,))

    freqs = grams['freq'].values
    phrases = grams['first'] + " " + grams['second']
    fmt = "@i"
    triee = marisa.RecordTrie(fmt, zip(phrases, freqs))

    # Store the trie
    with open('trie.pkl', 'wb') as output:
        pickle.dump(triee, output, pickle.HIGHEST_PROTOCOL)
    return triee


def one_letter(data_path):
    """
    Generate a trie that is used for a special case where only one letter is given
    to the autocomplete function. Since it's very expensive to go over all combinations
    each time, this function does it once and stores the result.
    :param data_path: path to the n-gram corpus
    :return: a one-letter trie, which also gets stored on the drive
    """
    with codecs.open(data_path, "r", encoding='utf-8', errors='ignore') as fdata:
        grams = pd.read_table(fdata, names=["freq", "first", "second"])

    global store_grams
    store_grams = grams.copy()

    short_grams = grams.copy()
    short_grams['first'] = short_grams['first'].apply(lambda x: x[0].lower())
    short_grams['indices'] = short_grams.index

    res = short_grams.groupby("first").apply(lambda group: group.nlargest(50, columns='freq'))
    indices = res['indices'].values

    grams = grams.iloc[indices, :]
    grams['freq'] = grams['freq'].apply(lambda x: (x,))

    freqs = grams['freq'].values
    phrases = grams['first'] + " " + grams['second']
    fmt = "@i"

    triee = marisa.RecordTrie(fmt, zip(phrases, freqs))
    with open('short_trie.pkl', 'wb') as output:
        pickle.dump(triee, output, pickle.HIGHEST_PROTOCOL)
    return triee


def popular_trie(data_path):
    """
    Generate a trie for the most popular words, like "to", "the", etc.
    Popular trie should be used if the branching factor for the long trie is large (>1000)
    :param data_path: path to the n-gram corpus
    :return: a popular trie, which also gets stored on the drive
    """
    with codecs.open(data_path, "r", encoding='utf-8', errors='ignore') as fdata:
        grams = pd.read_table(fdata, names=["freq", "first", "second"])

    try:
        long = open('trie.pkl', 'rb')
    except IOError:
        one_letter(data_path)
        long = open('trie.pkl', 'rb')

    triee = pickle.load(long)
    big_ones = set()
    for elem in set(grams['first'].values):
        if len(triee.items(elem)) > 7000:
            big_ones.add(elem)

    grams = grams.loc[grams['first'].isin(big_ones)]

    grams['freq'] = grams['freq'].apply(lambda x: (x,))

    freqs = grams['freq'].values
    phrases = grams['first'] + " " + grams['second']
    fmt = "@i"

    triee = marisa.RecordTrie(fmt, zip(phrases, freqs))
    with open('popular_trie.pkl', 'wb') as output:
        pickle.dump(triee, output, pickle.HIGHEST_PROTOCOL)
    with open('dict.pkl', 'wb') as output:
        pickle.dump(big_ones, output, pickle.HIGHEST_PROTOCOL)

    return triee

