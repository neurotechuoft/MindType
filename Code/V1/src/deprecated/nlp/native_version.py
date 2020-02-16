import codecs
import pandas as pd
import pytrie
import pickle


def native_load_data(path_to_data):
    """
    Load the longest version of the trie, containing most n-grams
    :param path_to_data: path to the n-gram corpus
    :return: the trie, which also gets stored on the drive
    """

    with codecs.open(path_to_data, "r", encoding='utf-8', errors='ignore') as fdata:
        grams = pd.read_table(fdata, names=["freq", "first", "second"])

    grams['freq'] = grams['freq'].apply(lambda x: (x,))
    freqs = grams['freq'].values
    phrases = grams['first'] + " " + grams['second']
    res = dict(zip(phrases, freqs))
    pytrie1 = pytrie.StringTrie(res)
    with open('pytrie.pkl', 'wb') as output:
        pickle.dump(pytrie1, output, pickle.HIGHEST_PROTOCOL)
    return pytrie1


def native_autocomplete(trie1, word):
    """
    Autocomplete the word/phrase using native python implementation of trie.
    If it's an incomplete word, then return the most likely completion.
    If it's a complete word, return the next word that is most likely.
    For now it's slower and less memory efficient than the C++ version,
    so use that one instead.
    :param word: (part of) a word
    :return: completed string
    """
    maxi = 0
    compl = ''
    for item in trie1.items(prefix = word):
        if item[1] > maxi:
            maxi = item[1]
            compl = item[0]
    if compl == '':
       return "couldn't find autocomplete for \"{}\"".format(word)
    longer = compl.split(' ')
    if len(longer) > 1 and longer[-2] in word:
        return longer[-1]
    return longer[0]


