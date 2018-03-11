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
        triee, popular_dict = check_cache(data_path, start_word)


    # Iterate over the trie elements that start with the start_word
    # and store the top 3 most frequent words
    item = triee.items(start_word)

    # complete_word = []
    # complete_freq = []
    # i = 0

    if len(start_word.split(" ")) < 1:
        next_word = next_word_indicator(item, start_word)
    else:
        next_word = False
        item = list(map(lambda x: (x[0].replace(start_word.split(" ")[0] + " ", ""), x[1]), item))
    # while len(item) > 0 and i < 3:
    #     highest_freq = 0
    #     for key, val in item:
    #         if val[0] > highest_freq:
    #             highest_freq = val[0]
    #             if key not in complete_word:
    #                 complete_word.append(key)
    #                 complete_freq.append(val)
    #     if not next_word:
    #         item = [(k, v) for k, v in item if complete_word[0].split(" ")[0] not in k]
    #     if complete_word[-1] in item:
    #         item.remove((complete_word[-1],complete_freq[-1]))
    #     i += 1


    # complete_freq_vals = list(map(lambda x: x[0], complete_freq))
    # complete_word_dict = dict(zip(complete_word, complete_freq_vals))
    complete_word_dict = dict(item)
    top_three = []
    while len(top_three) < 3:
        if len(complete_word_dict) > 0:
            pop_word = max(complete_word_dict, key=complete_word_dict.get)
            complete_word_dict.pop(pop_word, None)
            # print(pop_word)
        else:
            pop_word = max(popular_dict, key=popular_dict.get)
            popular_dict.pop(pop_word, None)

        if pop_word not in top_three:
            if not next_word:
                if pop_word.split(" ")[0] not in top_three:
                    top_three.append(pop_word.split(" ")[0])
            else:
                top_three.append(pop_word)

    complete_word = top_three

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

def next_word_indicator(item, word):
    for key, value in item:
        if key.split(" ")[0] == word.strip():
            return True

    return False

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
        return pickle.load(short), popular_dict
    if start_word in popular_dict:
        return pickle.load(pop_trie), popular_dict

    return pickle.load(long), popular_dict


def load_data(path_to_data, branch_limit=10000):
    """
    Load the longest version of the trie, containing most n-grams(limited by the branch_limit)
    :param path_to_data: path to the n-gram corpus
    :param branch_limit: the limit of children for each node of the trie. Default 10000
    :return: the trie, which also gets stored on the drive
    """

    with codecs.open(path_to_data, "r", encoding='utf-8', errors='ignore') as fdata:
        grams = pd.read_table(fdata, names=["freq", "first", "second"])
    # grams = pd.read_pickle('./resources/data.pkl')
    grams = grams.sort_values(by='freq', ascending=False)

    # Limit the number of children for each node
    grams = grams.groupby("first").head(branch_limit)

    # The transformation from int to a singular tuple is required by the trie API
    grams['freq'] = grams['freq'].apply(lambda x: (x,))

    freqs = grams['freq'].values
    phrases = grams['first'] + " " + grams['second']
    fmt = "@i"
    phrases = np.unicode(phrases.values)
    triee = marisa.RecordTrie(fmt, zip(phrases, freqs))

    # Store the trie
    with open('./resources/trie.pkl', 'wb') as output:
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
    # grams = pd.read_pickle('./resources/data.pkl')

    global store_grams
    store_grams = grams.copy()

    short_grams = grams.copy()
    # short_grams['first'] = short_grams[['first']].apply(lambda x: x[0].lower())
    short_grams['indices'] = short_grams.index

    res = short_grams.groupby("first").apply(lambda group: group.nlargest(50, columns='freq'))
    indices = res['indices'].values
    grams = grams.iloc[indices, :]
    grams['freq'] = grams['freq'].apply(lambda x: (x,))

    freqs = grams['freq'].values
    phrases = grams['first'] + " " + grams['second']
    fmt = "@i"
    phrases = np.unicode(phrases.values)
    triee = marisa.RecordTrie(fmt, zip(phrases, freqs))
    with open('./resources/short_trie.pkl', 'wb') as output:
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
    # grams = pd.read_pickle('./resources/data.pkl')

    try:
        long = open('./resources/trie.pkl', 'rb')
    except IOError:
        one_letter(data_path)
        long = open('./resources/trie.pkl', 'rb')

    triee = pickle.load(long)
    big_ones = dict()
    for elem in (grams.groupby(['first']).sum()).iterrows():
        count = elem[1]['freq']
        if count > 7000:
            big_ones[elem[1].name] = count
    grams = grams.loc[grams['first'].isin(big_ones)]

    grams['freq'] = grams['freq'].apply(lambda x: (x,))

    freqs = grams['freq'].values
    phrases = grams['first'] + " " + grams['second']
    fmt = "@i"
    phrases = np.unicode(phrases.values)
    triee = marisa.RecordTrie(fmt, zip(phrases, freqs))
    with open('./resources/popular_trie.pkl', 'wb') as output:
        pickle.dump(triee, output, pickle.HIGHEST_PROTOCOL)
    with open('./resources/dict.pkl', 'wb') as output:
        pickle.dump(big_ones, output, pickle.HIGHEST_PROTOCOL)

    return triee


if __name__ == "__main__":
    autocomplete("he", "random/w2_.txt")