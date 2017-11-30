import marisa_trie as marisa
import pandas as pd
import numpy as np
import codecs
import time
import pickle
import sys


# TODO: Need to rewrite the file read. Right now it assumes that only one text file is used.
# TODO: The easiest way is to probably change load_data to combine 2 and 3-grams(and maybe more)


def autocomplete(word, data_path, triee=None):
    start = time.time()
    if triee is None:
        triee = check_cache(data_path, word)

    maxi = 0
    compl = ''
    for key, val in triee.items(word):
        if val[0] > maxi:
            maxi = val[0]
            compl = key
    if compl == '':
        return "Couldn't find autocomplete for \"{}\"".format(word)
    longer = compl.split(' ')
    if len(longer) > 1 and longer[-2] in word:
        return longer[-1]
    return longer[0]


def check_cache(data_path, word):
    try:
        short = open('short_trie.pkl', 'rb')
    except IOError:
        one_letter(data_path)
        short = open('short_trie.pkl', 'rb')
    try:
        long = open('trie.pkl', 'rb')
    except IOError:
        load_data(data_path)
        long = open('trie.pkl', 'rb')

    try:
        pop_trie = open('popular_trie.pkl', 'rb')
        pop_dict = open('dict.pkl', 'rb')
        popular_dict = pickle.load(pop_dict)
    except IOError:
        popular_trie(data_path)
        pop_trie = open('popular_trie.pkl', 'rb')
        pop_dict = open('dict.pkl', 'rb')
        popular_dict = pickle.load(pop_dict)

    if len(word) == 1:
        return pickle.load(short)
    if word in popular_dict:
        return pickle.load(pop_trie)

    return pickle.load(long)


def load_data(path_to_data):
    with codecs.open(path_to_data, "r", encoding='utf-8', errors='ignore') as fdata:
        grams = pd.read_table(fdata, names=["freq", "first", "second"])

    grams = grams.sort_values(by='freq', ascending=False)
    grams = grams.groupby("first").head(10000)
    grams['freq'] = grams['freq'].apply(lambda x: (x,))

    freqs = grams['freq'].values
    phrases = grams['first'] + " " + grams['second']
    fmt = "@i"
    triee = marisa.RecordTrie(fmt, zip(phrases, freqs))
    with open('trie.pkl', 'wb') as output:
        pickle.dump(triee, output, pickle.HIGHEST_PROTOCOL)
    return triee


def one_letter(data_path):
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
